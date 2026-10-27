import json
import re
from collections import Counter
from pathlib import Path

path = Path("data/processed/urdu_shers_clean.jsonl")

if not path.exists():
    raise FileNotFoundError(f"Dataset not found: {path}")

script_counts = Counter()
word_counts = []
empty_responses = 0
multiline_responses = 0
examples = []
total = 0

def detect_script(text):
    devanagari = len(re.findall(r"[\u0900-\u097F]", text))
    arabic = len(re.findall(r"[\u0600-\u06FF]", text))
    latin = len(re.findall(r"[A-Za-z]", text))

    if devanagari > arabic and devanagari > latin:
        return "Hindi / Devanagari"
    if arabic > devanagari and arabic > latin:
        return "Arabic-script Urdu / Persian"
    if latin:
        return "Latin-script / Romanized"
    return "Other / unclear"

with path.open("r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue

        row = json.loads(line)
        prompt = row.get("prompt", "").strip()
        response = row.get("response", "").strip()
        total += 1

        script_counts[detect_script(response)] += 1
        word_counts.append(len(response.split()))

        if not response:
            empty_responses += 1
        if "\n" in response:
            multiline_responses += 1
        if len(examples) < 5:
            examples.append((prompt, response))

print("\n--- Sukoon AI Dataset Audit ---")
print("Total records:", total)
print("\nResponse script distribution:")

for script, count in script_counts.most_common():
    percentage = count / total * 100 if total else 0
    print(f"  {script}: {count} ({percentage:.1f}%)")

if word_counts:
    print("\nAverage response length (words):",
          round(sum(word_counts) / len(word_counts), 2))
    print("Shortest response (words):", min(word_counts))
    print("Longest response (words):", max(word_counts))

print("Empty responses:", empty_responses)
print("Responses containing line breaks:", multiline_responses)

print("\n--- Sample records ---")
for prompt, response in examples:
    print("\nPrompt:", prompt)
    print("Response:", response)
