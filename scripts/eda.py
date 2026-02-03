# import pandas as pd

# CSV_PATH = "data/processed/all_games.csv"

# df = pd.read_csv(CSV_PATH)

# # print(df.head())
# # print(df.shape)
# # print(df.info())
# # print(df.columns)
# # print(df.isna())
# # print(df["white_elo"].isna())
# # print(df["site"].isin(["?"]).sum())
# # df["date"] = df["date"].replace(
# #     r".*\?.*",
# #     pd.NA,
# #     regex=True
# # )

# cols = ["event","site","date","round","white","black","white_elo","black_elo","result","result_numeric","eco","total_moves","moves_san","moves_uci","elo_diff","source_file"]

# # for col in cols:
# #     df[col] = df[col].replace(r"\?", pd.NA, regex=True, inplace=True)

# # print(df.isin(["?"]).sum())
# # print(df.isna().sum())
# df[cols] = df[cols].replace(r"\?", pd.NA, regex=True)

# df.to_csv("all_games.csv", index=False)

import pandas as pd

# ---------- PATH ----------
CSV_PATH = "data/processed/all_games.csv"

# ---------- LOAD DATA ----------
df = pd.read_csv(CSV_PATH)

print("📊 Original shape:", df.shape)

# ---------- REPLACE '?' WITH NA ----------
# Replace '?' in ALL columns safely
df = df.replace(r"\?", pd.NA, regex=True)

# ---------- OPTIONAL: CHECK MISSING VALUES ----------
print("\n🔍 Missing values after cleaning:")
print(df.isna().sum())

# ---------- SAVE CLEANED DATA ----------
df.to_csv(CSV_PATH, index=False)

print("\n✅ '?' values replaced with NA and saved back to CSV")
print("📊 Final shape:", df.shape)
