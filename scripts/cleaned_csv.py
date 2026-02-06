import pandas as pd
import os

INPUT_DIR = "data/processed"
OUTPUT_FILE = "data/processed/all_players_clean.csv"

def normalize_name(name):
    return (
        str(name)
        .lower()
        .replace(",", "")
        .replace(" ", "")
        .strip()
    )

all_dfs = []

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".csv"):
        continue
    if file == "all_players_clean.csv":
        continue

    file_path = os.path.join(INPUT_DIR, file)
    df = pd.read_csv(file_path)

    # -------- extract & normalize player name --------
    raw_name = file.replace(".csv", "")
    player_name = raw_name.split("_")[0].strip()
    player_norm = normalize_name(player_name)

    df["player_name"] = player_name.lower()

    # -------- normalize white / black --------
    df["white"] = df["white"].astype(str).str.strip().str.lower()
    df["black"] = df["black"].astype(str).str.strip().str.lower()

    df["white_norm"] = df["white"].apply(normalize_name)
    df["black_norm"] = df["black"].apply(normalize_name)

    # -------- player & opponent --------
    df["player_color"] = ""
    df["opponent_name"] = ""
    df["opponent_color"] = ""

    mask_white = df["white_norm"].str.contains(player_norm, na=False)
    mask_black = df["black_norm"].str.contains(player_norm, na=False)

    df.loc[mask_white, "player_color"] = "White"
    df.loc[mask_white, "opponent_name"] = df.loc[mask_white, "black"]
    df.loc[mask_white, "opponent_color"] = "Black"

    df.loc[mask_black, "player_color"] = "Black"
    df.loc[mask_black, "opponent_name"] = df.loc[mask_black, "white"]
    df.loc[mask_black, "opponent_color"] = "White"

    # -------- year --------
    if "date" in df.columns:
        df["Year"] = df["date"].astype(str).str.slice(0, 4)
        df["Year"] = df["Year"].where(df["Year"].str.isnumeric(), "")
    else:
        df["Year"] = ""

    # -------- filter games before 2005 --------
    df["Year_num"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df[df["Year_num"] >= 2005]
    df = df.drop(columns=["Year_num"])

    # -------- player elo --------
    df["player_elo"] = pd.NA
    df.loc[mask_white, "player_elo"] = df.loc[mask_white, "white_elo"]
    df.loc[mask_black, "player_elo"] = df.loc[mask_black, "black_elo"]
    df["player_elo"] = pd.to_numeric(df["player_elo"], errors="coerce")

    # -------- opponent elo --------
    df["opponent_elo"] = pd.NA
    df.loc[mask_white, "opponent_elo"] = df.loc[mask_white, "black_elo"]
    df.loc[mask_black, "opponent_elo"] = df.loc[mask_black, "white_elo"]

    # -------- final result --------
    df["final_result"] = "Draw"

    df.loc[(df["player_color"] == "White") & (df["result"] == "1-0"), "final_result"] = "Win"
    df.loc[(df["player_color"] == "White") & (df["result"] == "0-1"), "final_result"] = "Loss"
    df.loc[(df["player_color"] == "Black") & (df["result"] == "0-1"), "final_result"] = "Win"
    df.loc[(df["player_color"] == "Black") & (df["result"] == "1-0"), "final_result"] = "Loss"

    # -------- cleanup --------
    df = df.drop(columns=["date", "moves_san", "moves_uci", "white_norm", "black_norm"], errors="ignore")

    unwanted_keywords = [
        "rapid", "speed", "blitz", "online", "bullet", "armageddon",
        "chess.com", "chess24", "titled tuesday", "titled tue",
        "mrdodgy", "chessable masters"
    ]

    pattern = "|".join(unwanted_keywords)
    df = df[~df["event"].str.contains(pattern, case=False, na=False)]

    all_dfs.append(df)

# -------- merge & save --------
final_df = pd.concat(all_dfs, ignore_index=True)
final_df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ All files processed & merged → {OUTPUT_FILE}")
print(f"♟️ Total games: {len(final_df)}")


# For single process 

# import pandas as pd
# import os
# import datetime

# file_path = "data/processed/Li.csv"
# df = pd.read_csv(file_path)

# # extract player name
# file_name = os.path.basename(file_path).replace(".csv", "")

# # normalize strings (VERY IMPORTANT)
# df["white"] = df["white"].astype(str).str.strip().str.lower()
# df["black"] = df["black"].astype(str).str.strip().str.lower()
# file_name = file_name.strip().lower()

# # add file_name column
# df["player_name"] = file_name

# # create player_color
# df["player_color"] = ""

# df.loc[df["white"].str.contains(file_name, na=False), "player_color"] = "White"
# df.loc[df["black"].str.contains(file_name, na=False), "player_color"] = "Black"

# # normalize name columns
# df["white"] = df["white"].astype(str).str.strip().str.lower()
# df["black"] = df["black"].astype(str).str.strip().str.lower()

# df["opponent_name"] = ""

# # player is White
# mask_white = df["white"].str.contains(file_name, na=False)
# df.loc[mask_white, "player_color"] = "White"
# df.loc[mask_white, "opponent_name"] = df.loc[mask_white, "black"]

# # player is Black
# mask_black = df["black"].str.contains(file_name, na=False)
# df.loc[mask_black, "player_color"] = "Black"
# df.loc[mask_black, "opponent_name"] = df.loc[mask_black, "white"]

# # create opponent_color
# df["opponent_color"] = ""

# df.loc[df["white"].str.contains(file_name, na=False), "opponent_color"] = "Black"
# df.loc[df["black"].str.contains(file_name, na=False), "opponent_color"] = "White"

# # extract only year
# df["Year"] = df["date"].astype(str).str.slice(0, 4)

# # replace invalid years
# df["Year"] = df["Year"].where(df["Year"].str.isnumeric(), "")

# df["player_elo"] = pd.NA

# mask_player_white = df["white"].str.contains(file_name, na=False)
# df.loc[mask_player_white, "player_elo"] = df.loc[mask_player_white, "white_elo"]

# mask_player_black = df["black"].str.contains(file_name, na=False)
# df.loc[mask_player_black, "player_elo"] = df.loc[mask_player_black, "black_elo"]

# df["player_elo"] = pd.to_numeric(df["player_elo"], errors="coerce")


# df["opponent_elo"] = pd.NA

# mask_opponent_white = df["white"] == df["opponent_name"]
# df.loc[mask_opponent_white, "opponent_elo"] = df.loc[mask_opponent_white, "white_elo"]

# mask_opponent_black = df["black"] == df["opponent_name"]
# df.loc[mask_opponent_black, "opponent_elo"] = df.loc[mask_opponent_black, "black_elo"]

# df["final_result"] = "Draw"   # default

# mask_white = df["player_color"] == "White"

# df.loc[mask_white & (df["result"] == "1-0"), "final_result"] = "Win"
# df.loc[mask_white & (df["result"] == "0-1"), "final_result"] = "Loss"

# mask_black = df["player_color"] == "Black"

# df.loc[mask_black & (df["result"] == "0-1"), "final_result"] = "Win"
# df.loc[mask_black & (df["result"] == "1-0"), "final_result"] = "Loss"


# df = df.drop(columns=["date","moves_san","moves_uci"])

# # List of unwanted keywords
# unwanted_keywords = [
#     "rapid", "speed", "blitz", "online", "bullet", "armageddon",
#     "chess.com", "chess24", "titled tuesday", "titled tue",
#     "mrdodgy", "chessable masters"
# ]

# # Create regex pattern
# pattern = "|".join(unwanted_keywords)

# # Remove rows where event contains any of these words
# df = df[~df["event"].str.contains(pattern, case=False, na=False)]

# # save
# df.to_csv("data/processed/Li_1.csv", index=False)

# print("✅  added successfully")


