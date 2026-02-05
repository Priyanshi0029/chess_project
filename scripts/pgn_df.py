import chess.pgn
import pandas as pd
import os

RAW_PGN_DIR = "data/raw_pgn"
OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

result_map = {
    "1-0": 1,
    "0-1": -1,
    "1/2-1/2": 0
}

for pgn_file in os.listdir(RAW_PGN_DIR):

    if not pgn_file.endswith(".pgn"):
        continue

    print(f"Processing {pgn_file}...")

    games_data = []

    pgn_path = os.path.join(RAW_PGN_DIR, pgn_file)
    output_csv = os.path.join(
        OUTPUT_DIR,
        pgn_file.replace(".pgn", ".csv")
    )

    with open(pgn_path, encoding="latin-1") as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            h = game.headers
            board = game.board()

            san_moves = []
            uci_moves = []

            for move in game.mainline_moves():
                san_moves.append(board.san(move))
                uci_moves.append(move.uci())
                board.push(move)

            games_data.append({
                "event": h.get("Event"),
                "site": h.get("Site"),
                "date": h.get("Date"),
                "round": h.get("Round"),
                "white": h.get("White"),
                "black": h.get("Black"),
                "white_elo": h.get("WhiteElo"),
                "black_elo": h.get("BlackElo"),
                "result": h.get("Result"),
                "result_numeric": result_map.get(h.get("Result")),
                "eco": h.get("ECO"),
                "total_moves": len(uci_moves),
                "moves_san": " ".join(san_moves),
                "moves_uci": " ".join(uci_moves)
            })

    df = pd.DataFrame(games_data)

    df["white_elo"] = pd.to_numeric(df["white_elo"], errors="coerce")
    df["black_elo"] = pd.to_numeric(df["black_elo"], errors="coerce")
    df["elo_diff"] = df["white_elo"] - df["black_elo"]

    df.dropna(subset=["white", "black", "result"], inplace=True)

    df.to_csv(output_csv, index=False)

    print(f"✅ Saved {len(df)} games → {output_csv}")

print("\n🎉 All PGN files processed successfully!")
