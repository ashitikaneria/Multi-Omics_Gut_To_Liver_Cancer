#!/usr/bin/env python3
"""
Fetch & filter SRA metadata for BioProject PRJNA872871
Uses NCBI RunInfo CSV (far more reliable than raw XML parsing)

Extracts: Healthy Control & Advanced Liver Disease samples

Requirements:
    pip install requests pandas
"""

import requests
import pandas as pd
import time
import sys
import os
import io

# ─────────────────────────────────────────────────────────────────
# CONFIG — edit here if needed
# ─────────────────────────────────────────────────────────────────
BIOPROJECT  = "PRJNA872871"
EMAIL       = "your_email@example.com"   # ← change (NCBI best practice)
BASE_EUTIL  = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# What we want to keep — case-insensitive, partial match
TARGET_GROUPS = [
    "healthy control",
    "advanced liver disease",
]

OUTPUT_TSV   = "filtered_metadata.tsv"
SRR_LIST     = "srr_list.txt"
DOWNLOAD_SH  = "download_fastq.sh"
ALL_META_TSV = "all_metadata.tsv"   # full project metadata for reference

# ─────────────────────────────────────────────────────────────────
# STEP 1 — Search SRA and get WebEnv + query_key (history server)
# ─────────────────────────────────────────────────────────────────
def search_with_history(bioproject):
    print(f"\n[1/4] Searching SRA for {bioproject} ...")
    params = {
        "db"         : "sra",
        "term"       : f"{bioproject}[BioProject]",
        "usehistory" : "y",
        "retmode"    : "json",
        "retmax"     : "5000",
        "email"      : EMAIL,
    }
    r = requests.get(f"{BASE_EUTIL}/esearch.fcgi", params=params, timeout=60)
    r.raise_for_status()
    data = r.json()["esearchresult"]
    count   = int(data["count"])
    webenv  = data["webenv"]
    qkey    = data["querykey"]
    print(f"      Found {count} SRA records.")
    return count, webenv, qkey

# ─────────────────────────────────────────────────────────────────
# STEP 2 — Fetch RunInfo CSV (comma-separated, very clean)
# ─────────────────────────────────────────────────────────────────
def fetch_runinfo_csv(count, webenv, qkey):
    print(f"[2/4] Fetching RunInfo CSV for all {count} records ...")
    params = {
        "db"        : "sra",
        "WebEnv"    : webenv,
        "query_key" : qkey,
        "rettype"   : "runinfo",
        "retmode"   : "text",
        "retmax"    : str(count),
        "retstart"  : "0",
        "email"     : EMAIL,
    }
    time.sleep(0.4)
    r = requests.get(f"{BASE_EUTIL}/efetch.fcgi", params=params, timeout=120)
    r.raise_for_status()

    csv_text = r.text.strip()
    if not csv_text or csv_text.startswith("<?xml"):
        raise ValueError("NCBI returned XML instead of CSV — runinfo format unavailable. Try again.")

    df = pd.read_csv(io.StringIO(csv_text))
    print(f"      Loaded {len(df)} runs with {len(df.columns)} columns.")
    return df

# ─────────────────────────────────────────────────────────────────
# STEP 3 — Show all groups and filter targets
# ─────────────────────────────────────────────────────────────────
def show_all_groups(df):
    print("\n" + "="*60)
    print("ALL SAMPLE GROUPS IN THIS PROJECT:")
    print("="*60)

    # RunInfo CSV uses these columns for sample metadata
    for col in ["disease_state", "Disease_state", "source_name",
                "SampleName", "LibraryName", "BioSample", "tissue",
                "cell_type", "phenotype", "subject_status"]:
        if col in df.columns:
            print(f"\n  Column: '{col}'")
            for val, cnt in df[col].value_counts().items():
                print(f"    {cnt:>4}x  {val}")

def filter_targets(df, targets):
    print(f"\n[3/4] Filtering for target groups ...")

    # Build a combined search string from all text-like columns
    str_cols = df.select_dtypes(include="object").columns.tolist()
    df["_combined"] = df[str_cols].fillna("").agg(" | ".join, axis=1).str.lower()

    masks = [df["_combined"].str.contains(t.lower(), regex=False) for t in targets]
    mask  = masks[0]
    for m in masks[1:]:
        mask = mask | m

    filtered = df[mask].drop(columns=["_combined"]).copy()
    df.drop(columns=["_combined"], inplace=True)
    print(f"      Matched {len(filtered)} runs.")
    return filtered

# ─────────────────────────────────────────────────────────────────
# STEP 4 — Save outputs
# ─────────────────────────────────────────────────────────────────
def save_outputs(df_all, df_filt):
    # Save full metadata for reference
    df_all.to_csv(ALL_META_TSV, sep="\t", index=False)
    print(f"\n[4/4] Saving outputs ...")
    print(f"      Full metadata   → {ALL_META_TSV}")

    if df_filt.empty:
        print("\n  ⚠  No samples matched the target groups!")
        print("  → Check the 'ALL SAMPLE GROUPS' printout above.")
        print("  → Copy the exact group labels and update TARGET_GROUPS in this script.")
        return

    # Show filtered group summary
    print("\n" + "="*60)
    print("FILTERED SAMPLES SUMMARY:")
    print("="*60)
    for col in ["disease_state", "Disease_state", "source_name",
                "SampleName", "LibraryName", "tissue", "subject_status"]:
        if col in df_filt.columns and df_filt[col].nunique() > 0:
            print(f"\n  [{col}]:")
            for val, cnt in df_filt[col].value_counts().items():
                print(f"    {cnt:>4}x  {val}")

    # Save filtered metadata
    df_filt.to_csv(OUTPUT_TSV, sep="\t", index=False)
    print(f"\n  Filtered metadata → {OUTPUT_TSV}")

    # Save SRR list
    srr_col = "Run" if "Run" in df_filt.columns else df_filt.columns[0]
    srr_list = df_filt[srr_col].dropna().tolist()
    with open(SRR_LIST, "w") as f:
        f.write("\n".join(srr_list) + "\n")
    print(f"  SRR list          → {SRR_LIST}  ({len(srr_list)} accessions)")
    print(f"\n  SRR accessions:")
    for s in srr_list:
        print(f"    {s}")

    # Generate download script
    write_download_script(srr_list)

def write_download_script(srr_list):
    lines = [
        "#!/usr/bin/env bash",
        "# Auto-generated download script for filtered SRR accessions",
        "# Requirements: SRA Toolkit",
        "#   conda install -c bioconda sra-tools",
        "#   OR: sudo apt-get install sra-toolkit",
        "",
        "set -euo pipefail",
        'OUTDIR="${1:-fastq_output}"',
        'mkdir -p "$OUTDIR"',
        f'echo "Downloading {len(srr_list)} SRR accessions to $OUTDIR ..."',
        "",
    ]
    for srr in srr_list:
        lines += [
            f'echo "\\n--- Downloading {srr} ---"',
            f'prefetch {srr} --output-directory "$OUTDIR"',
            f'fasterq-dump "$OUTDIR/{srr}" --outdir "$OUTDIR" --split-files --threads 4',
            f'pigz -p 4 "$OUTDIR"/{srr}*.fastq 2>/dev/null || gzip "$OUTDIR"/{srr}*.fastq',
            "",
        ]
    lines += [
        'echo "\\nAll downloads complete. Files in: $OUTDIR"',
        "",
    ]
    with open(DOWNLOAD_SH, "w") as f:
        f.write("\n".join(lines))
    os.chmod(DOWNLOAD_SH, 0o755)
    print(f"  Download script   → {DOWNLOAD_SH}")
    print(f"\n  To download all FASTQs:")
    print(f"      bash {DOWNLOAD_SH} /path/to/output/folder")

# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────
def main():
    print("="*60)
    print(f"  SRA RunInfo Fetcher  |  BioProject: {BIOPROJECT}")
    print("="*60)

    try:
        count, webenv, qkey = search_with_history(BIOPROJECT)
        df_all = fetch_runinfo_csv(count, webenv, qkey)
        show_all_groups(df_all)
        df_filt = filter_targets(df_all, TARGET_GROUPS)
        save_outputs(df_all, df_filt)

    except requests.HTTPError as e:
        print(f"\n  HTTP Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n  Data Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n  Interrupted.")
        sys.exit(0)

    print("\nDone.\n")

if __name__ == "__main__":
    main()
