import os
import pandas as pd

input_folder = "filt_data"

samples = set()

for fname in os.listdir(input_folder):
    if fname.endswith("_1.fastq"):
        samples.add(fname.replace("_1.fastq", ""))
    elif fname.endswith("_2.fastq"):
        samples.add(fname.replace("_2.fastq", ""))

samples = sorted(samples)

df = pd.DataFrame({"sample_name": samples})
df.to_excel("sample_names.xlsx", index=False)

print(df)
