import pandas as pd
import numpy as np
import re

input_file = "func.KO.abd.xlsx"
output_file = "kegg_pathway_abundance_comparison.xlsx"

df = pd.read_excel(input_file, sheet_name="func.KO")
df.columns = [str(c).strip() for c in df.columns]

sample_col = df.columns[0]
type_col = df.columns[1]

kegg_cols = [c for c in df.columns[2:] if re.match(r"^K\d+", str(c))]

for c in kegg_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

g = (
    df[type_col]
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
)

adv_mask = g.eq("advance liver disease")
healthy_mask = g.eq("healthy control")

print("Advance liver disease samples:", int(adv_mask.sum()))
print("Healthy control samples:", int(healthy_mask.sum()))

if adv_mask.sum() == 0 or healthy_mask.sum() == 0:
    raise ValueError("Group matching failed. Check Type column labels.")

res = pd.DataFrame({"KEGG_ID": kegg_cols})

res["Advance_mean"] = [df.loc[adv_mask, k].mean(skipna=True) for k in kegg_cols]
res["Healthy_mean"] = [df.loc[healthy_mask, k].mean(skipna=True) for k in kegg_cols]

res["Advance_sum"] = [df.loc[adv_mask, k].sum(skipna=True) for k in kegg_cols]
res["Healthy_sum"] = [df.loc[healthy_mask, k].sum(skipna=True) for k in kegg_cols]

res["Advance_median"] = [df.loc[adv_mask, k].median(skipna=True) for k in kegg_cols]
res["Healthy_median"] = [df.loc[healthy_mask, k].median(skipna=True) for k in kegg_cols]

res["Mean_difference"] = res["Advance_mean"] - res["Healthy_mean"]
res["Sum_difference"] = res["Advance_sum"] - res["Healthy_sum"]

res["Mean_fold_change_Advance_vs_Healthy"] = np.where(
    res["Healthy_mean"] > 0,
    res["Advance_mean"] / res["Healthy_mean"],
    np.nan
)

res["More_abundant_in"] = np.where(
    res["Advance_mean"] > res["Healthy_mean"],
    "Advance liver disease",
    np.where(
        res["Advance_mean"] < res["Healthy_mean"],
        "Healthy control",
        "Equal"
    )
)

res["Nonzero_in_Advance"] = [
    int((df.loc[adv_mask, k].fillna(0) > 0).sum()) for k in kegg_cols
]
res["Nonzero_in_Healthy"] = [
    int((df.loc[healthy_mask, k].fillna(0) > 0).sum()) for k in kegg_cols
]

res["Percent_nonzero_Advance"] = (res["Nonzero_in_Advance"] / int(adv_mask.sum())) * 100
res["Percent_nonzero_Healthy"] = (res["Nonzero_in_Healthy"] / int(healthy_mask.sum())) * 100

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    res.to_excel(writer, sheet_name="All_KEGG_compare", index=False)

    res[res["More_abundant_in"] == "Advance liver disease"].to_excel(
        writer, sheet_name="Higher_in_Advance", index=False
    )

    res[res["More_abundant_in"] == "Healthy control"].to_excel(
        writer, sheet_name="Higher_in_Healthy", index=False
    )

    summary = pd.DataFrame({
        "Metric": [
            "Input file",
            "Sheet used",
            "Advance liver disease samples",
            "Healthy control samples",
            "Total KEGG IDs"
        ],
        "Value": [
            input_file,
            "func.KO",
            int(adv_mask.sum()),
            int(healthy_mask.sum()),
            len(kegg_cols)
        ]
    })
    summary.to_excel(writer, sheet_name="Summary", index=False)

print(f"Saved: {output_file}")
