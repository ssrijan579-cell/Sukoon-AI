
import json
import random
from pathlib import Path

SOURCE = Path("data/processed/urdu_shers_clean.jsonl")
OUTPUT_DIR = Path("data/processed/splits")
SEED = 42

def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing dataset: {SOURCE}")

    records = []
    with SOURCE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    # Basic schema validation
    records = [
        row for row in records
        if isinstance(row.get("prompt"), str)
        and row["prompt"].strip()
        and isinstance(row.get("response"), str)
        and row["response"].strip()
    ]

    random.Random(SEED).shuffle(records)

    total = len(records)
    train_end = int(total * 0.80)
    val_end = train_end + int(total * 0.10)

    splits = {
        "train": records[:train_end],
        "validation": records[train_end:val_end],
        "test": records[val_end:],
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for name, rows in splits.items():
        path = OUTPUT_DIR / f"{name}.jsonl"
        with path.open("w", encoding="utf-8") as file:
            for row in rows:
                file.write(
                    json.dumps(row, ensure_ascii=False) + "\n"
                )
        print(f"{name}: {len(rows)} records -> {path}")

    print(f"Total split records: {sum(map(len, splits.values()))}")
    print(f"Random seed: {SEED}")

if __name__ == "__main__":
    main()
