import pandas as pd
import re
# ---------- PATH ----------
CSV_PATH = "data/processed/Yu.csv"
df = pd.read_csv(CSV_PATH)
player_name = "Yu Yangyi"

df["player_color"] = df.apply(
    lambda row: "White" if row["white"] == player_name else "Black",
    axis=1
)

df.to_csv(CSV_PATH, index=False)