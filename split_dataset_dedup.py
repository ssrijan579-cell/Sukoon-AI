import json
import random
import unicodedata
from pathlib import Path

INPUT_FILE = Path("data/processed/urdu_shers_clean.jsonl")
OUTPUT_DIR = Path("data/processed/splits_dedup")

SEED = 42
TRAIN_RATIO = 0.80
VALIDATION_RATIO = 0.10


def normalize_response(text):
    text = unicodedata.normalize("NFKC", text)
    return " ".join(text.casefold().split())


def load_records(path):
    with path.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {INPUT_FILE}\n"
            "Check that prepare_dataset.py has already run."
        )

    records = load_records(INPUT_FILE)
    original_count = len(records)

    unique_records = []
    seen_responses = set()
    empty_count = 0
    duplicate_count = 0

    for record in records:
        response = record.get("response", "")

        if not isinstance(response, str) or not response.strip():
            empty_count += 1
            continue

        normalized = normalize_response(response)

        if normalized in seen_responses:
            duplicate_count += 1
            continue

        seen_responses.add(normalized)
        unique_records.append(record)

    random.Random(SEED).shuffle(unique_records)

    total = len(unique_records)
    train_end = int(total * TRAIN_RATIO)
    validation_end = train_end + int(total * VALIDATION_RATIO)

    splits = {
        "train": unique_records[:train_end],
        "validation": unique_records[train_end:validation_end],
        "test": unique_records[validation_end:],
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for split_name, split_records in splits.items():
        output_file = OUTPUT_DIR / f"{split_name}.jsonl"

        with output_file.open("w", encoding="utf-8") as file:
            for record in split_records:
                file.write(
                    json.dumps(record, ensure_ascii=False) + "\n"
                )

        print(f"{split_name}: {len(split_records)} records -> {output_file}")

    print("\n--- Deduplication Summary ---")
    print(f"Original records: {original_count}")
    print(f"Empty responses removed: {empty_count}")
    print(f"Duplicate responses removed: {duplicate_count}")
    print(f"Unique records retained: {len(unique_records)}")
    print(f"Random seed: {SEED}")


if __name__ == "__main__":
    main()
