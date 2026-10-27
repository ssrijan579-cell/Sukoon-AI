
import json
from pathlib import Path

BASE = Path("data/processed/splits")

def load_records(name):
    path = BASE / f"{name}.jsonl"
    with path.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]

train = load_records("train")
validation = load_records("validation")
test = load_records("test")

def response_set(records):
    return {
        " ".join(row["response"].lower().split())
        for row in records
        if row.get("response", "").strip()
    }

train_responses = response_set(train)
val_responses = response_set(validation)
test_responses = response_set(test)

checks = [
    ("Train vs validation", train_responses, val_responses),
    ("Train vs test", train_responses, test_responses),
    ("Validation vs test", val_responses, test_responses),
]

print("--- Exact Response Leakage Check ---")

for name, first, second in checks:
    overlap = first & second
    print(f"{name}: {len(overlap)} shared responses")

print("\nSplit sizes:")
print("Train:", len(train))
print("Validation:", len(validation))
print("Test:", len(test))
