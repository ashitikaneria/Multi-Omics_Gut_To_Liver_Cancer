import os
import json
import pandas as pd

rows = []

# Walk through ALL subfolders to find JSON files
for root, dirs, files in os.walk("."):
    for fname in files:
        if fname.lower().endswith(".json"):
            json_path = os.path.join(root, fname)
            
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    j = json.load(f)
                
                sample_name = os.path.splitext(fname)[0]
                folder_name = os.path.basename(root)
                
                # Use folder name as sample name if available
                if folder_name != "." and folder_name != "fastp_output":
                    sample_name = folder_name

                bf = j.get("summary", {}).get("before_filtering", {})
                af = j.get("summary", {}).get("after_filtering", {})
                fr = j.get("filtering_result", {})

                before_reads = bf.get("total_reads")
                after_reads = af.get("total_reads")
                passed_reads = fr.get("passed_filter_reads")

                if before_reads not in [None, 0] and passed_reads is not None:
                    passed_pct = round((passed_reads / before_reads) * 100, 6)
                    loss_pct = round(100 - passed_pct, 6)
                else:
                    passed_pct = None
                    loss_pct = None

                rows.append({
                    "json_file": fname,
                    "sample_name": sample_name,
                    "folder_path": root,
                    "before_filtering_total_reads": before_reads,
                    "after_filtering_total_reads": after_reads,
                    "reads_passed_filters_count": passed_reads,
                    "reads_passed_filters_percent": passed_pct,
                    "reads_loss_percent": loss_pct
                })
                
            except Exception as e:
                print(f"Error reading {json_path}: {e}")

print(f"Found {len(rows)} JSON files across all subfolders")

df = pd.DataFrame(rows)
df = df.sort_values("sample_name")
df.to_excel("fastp_summary.xlsx", index=False)

print(f"✅ Created fastp_summary.xlsx with {len(df)} samples")
