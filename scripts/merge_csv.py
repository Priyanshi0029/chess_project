import pandas as pd
import os

PROCESSED_DIR = "data/processed"
OUTPUT_FILE = "data/processed/all_games.csv"

csv_files = [
    f for f in os.listdir(PROCESSED_DIR)
    if f.endswith(".csv") and f != "all_games.csv"
]

df_list = []

for file in csv_files:
    file_path = os.path.join(PROCESSED_DIR, file)
    df = pd.read_csv(file_path)
    df["source_file"] = file.replace(".csv", "")  # optional
    df_list.append(df)

merged_df = pd.concat(df_list, ignore_index=True)

merged_df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Merged {len(csv_files)} files into {OUTPUT_FILE}")
print(f"📊 Total games: {len(merged_df)}")
