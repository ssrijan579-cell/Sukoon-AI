from datasets import load_dataset
from pathlib import Path

dataset_name = "keplersystems/UrduShers-10k"
output = Path("data/raw/urdu_shers_raw.jsonl")
output.parent.mkdir(parents=True, exist_ok=True)

print(f"Loading dataset: {dataset_name}")

dataset = load_dataset(dataset_name, split="train")

print("Rows:", len(dataset))
print("Columns:", dataset.column_names)
print("First record:")
print(dataset[0])

dataset.to_json(
    str(output),
    orient="records",
    force_ascii=False,
)

print(f"Saved dataset to: {output}")
