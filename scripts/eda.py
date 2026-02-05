

# print(df.isna())
# print(df["white_elo"].isna())
# print(df["site"].isin(["?"]).sum())
# df["date"] = df["date"].replace(
#     r".*\?.*",
#     pd.NA,
#     regex=True
# )

# cols = ["event","site","date","round","white","black","white_elo","black_elo","result","result_numeric","eco","total_moves","moves_san","moves_uci","elo_diff","source_file"]

# for col in cols:
#     df[col] = df[col].replace(r"\?", pd.NA, regex=True, inplace=True)

# print(df.isin(["?"]).sum())
# print(df.isna().sum())
# df[cols] = df[cols].replace(r"\?", pd.NA, regex=True)


import pandas as pd
import re
# ---------- PATH ----------
CSV_PATH = "data/processed/Yu.csv"

# ---------- LOAD DATA ----------
df = pd.read_csv(CSV_PATH)

# print("📊 Original shape:", df.shape)

# ---------- REPLACE '?' WITH NA ----------
# Replace '?' in ALL columns safely
# df = df.replace(r"\?", pd.NA, regex=True)

# ---------- OPTIONAL: CHECK MISSING VALUES ----------
# print("\n🔍 Missing values after cleaning:")
# print(df.isna().sum())
# print(df.head())
# print(df.shape)
# print(df.info())
# print(df.columns)
# print(df.describe)


# df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
# print(df["white"].unique())

# df["round"] = df["round"].fillna(0)
# print(df["round"].isna().sum())

# df = df.rename(columns={
#     "Player_Name":"white" ,
#     "Opponent_Name":"black",
#     "Player_Elo": "white_elo",
#     "Opponent_Elo": "black_elo",
# })


# result_map = {
#     "1-0": "White",
#     "0-1": "Black",
#     "1/2-1/2": "Draw"
# }

# df["result"] = df["result"].map(result_map)



# List of unwanted keywords
unwanted_keywords = [
    "rapid", "speed", "blitz", "online", "bullet", "armageddon",
    "chess.com", "chess24", "titled tuesday", "titled tue",
    "mrdodgy", "chessable masters"
]

# Create regex pattern
pattern = "|".join(unwanted_keywords)

# Remove rows where event contains any of these words
df = df[~df["event"].str.contains(pattern, case=False, na=False)]

player_name = "Yu Yangyi"

df["player_color"] = df.apply(
    lambda row: "White" if row["white"] == player_name else "Black",
    axis=1
)
# remove moves_san and moves_uci columns
# df = df.drop(columns=["moves_san","moves_uci"])
# df = df.drop(columns=["source_file"])
# # ---------- SAVE CLEANED DATA ----------
df.to_csv(CSV_PATH, index=False)

# print("\n✅ '?' values replaced with NA and saved back to CSV")
# print("📊 Final shape:", df.shape)




