import pandas as pd
import requests
import time

# Load your EXISTING mapping file
df = pd.read_excel("KO_pathway_mapping.xlsx")

# Function to get SYMBOL + NAME
def get_ko_info(ko):
    try:
        res = requests.get(f"http://rest.kegg.jp/get/{ko}")

        symbol = "NA"
        name = "NA"

        if res.status_code == 200:
            for line in res.text.split("\n"):
                if line.startswith("SYMBOL"):
                    symbol = line.replace("SYMBOL", "").strip()
                elif line.startswith("NAME"):
                    name = line.replace("NAME", "").strip()

        return symbol, name

    except:
        return "NA", "NA"


# Lists to store results
symbols = []
names = []

# Loop through KO_ID column
for ko in df["KO_ID"]:
    ko = str(ko).strip().upper()
    print(f"Processing {ko}...")

    symbol, name = get_ko_info(ko)

    symbols.append(symbol)
    names.append(name)

    time.sleep(0.3)

# Add new columns AFTER Pathways
df["Symbol"] = symbols
df["Name"] = names

# Save new file
df.to_excel("KO_full_annotation.xlsx", index=False)

print("✅ Done! Added Symbol and Name columns.")
