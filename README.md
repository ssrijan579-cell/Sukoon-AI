# Sukoon AI

A multilingual AI shayari platform focused on poetry generation, continuation, and understanding.

## Planned Features
- Shayari generation and continuation
- Hindi, Urdu, Romanized Hindi/Urdu, and English support
- NLP-based poetry analysis
- Model evaluation and an interactive application

## Current Progress
- [x] Downloaded an initial Urdu shayari dataset
- [x] Cleaned prompt-response records
- [x] Audited the dataset
- [x] Created train, validation, and test splits
- [x] Checked exact response overlap across splits
- [ ] Build a leakage-safe dataset pipeline
- [ ] Develop baseline NLP models
- [ ] Evaluate a shayari generation model
- [ ] Build and deploy the application

## Project Structure
- `data/`
- `download_dataset.py`
- `prepare_dataset.py`
- `audit_dataset.py`
- `split_dataset.py`
- `check_split_leakage.py`
- `README.md`
- `.gitignore`

## Setup
Activate the existing environment:

`conda activate sukoon-ai`

## Dataset
Initial dataset: `keplersystems/UrduShers-10k` from Hugging Face. Verify its license and attribution requirements before redistributing data or publishing a model trained on it.

## Status
This project is under active development.
