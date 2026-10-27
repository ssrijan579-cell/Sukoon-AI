import json
from pathlib import Path

source = Path("data/raw/urdu_shers_raw.jsonl")
output = Path("data/processed/urdu_shers_clean.jsonl")
output.parent.mkdir(parents=True, exist_ok=True)

cleaned = []
seen = set()
empty_records = 0
duplicates = 0

with source.open("r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue

        record = json.loads(line)
        messages = record.get("messages", [])

        prompt = ""
        response = ""

        for message in messages:
            role = message.get("role")
            content = message.get("content", "")

            if not isinstance(content, str):
                continue

            content = content.strip()

            if role == "user" and not prompt:
                prompt = content
            elif role == "assistant" and not response:
                response = content

        if not prompt or not response:
            empty_records += 1
            continue

        key = (prompt, response)
        if key in seen:
            duplicates += 1
            continue

        seen.add(key)
        cleaned.append({
            "prompt": prompt,
            "response": response
        })

with output.open("w", encoding="utf-8") as f:
    for record in cleaned:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

print("\n--- Dataset Preparation Report ---")
print("Original file:", source)
print("Clean records:", len(cleaned))
print("Incomplete records skipped:", empty_records)
print("Duplicate pairs removed:", duplicates)
print("Output file:", output)

print("\n--- Three Sample Records ---")
for record in cleaned[:3]:
    print(json.dumps(record, ensure_ascii=False, indent=2))
