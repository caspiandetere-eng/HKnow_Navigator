"""Dynamic healthcare dataset acquisition engine.

Fetches, normalizes, and saves clinical datasets from Hugging Face into
data/raw/.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Callable
from datasets import load_dataset

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def _safe_str(val: Any) -> str:
  """Safely converts and strips nullable fields."""
  if val is None:
    return ""
  return str(val).strip()


DATASET_REGISTRY: dict[str, dict[str, Any]] = {
    "medquad": {
        "hf_repo": "lavita/MedQuAD",
        "split": "train",
        "source": "NIH",
        "document_type": "faq",
        "output_file": "medquad_dataset.json",
        "builder": lambda item, idx: {
            "document_id": f"medquad_{idx + 1:05d}",
            "content": (
                f"Question: {_safe_str(item.get('question'))}\n\nAnswer:"
                f" {_safe_str(item.get('Answer'))}"
            ),
            "metadata": {
                "source": "NIH",
                "title": _safe_str(item.get("question"))[:100]
                or f"NIH Record {idx + 1}",
                "url": item.get("URL"),
                "document_type": "faq",
                "category": _safe_str(item.get("Focus_area")) or "general",
            },
        },
    },
    "pubmed_qa": {
        "hf_repo": "llamafactory/PubMedQA",
        "split": "train",
        "source": "PubMed",
        "document_type": "article",
        "output_file": "pubmed_dataset.json",
        "builder": lambda item, idx: {
            "document_id": f"pubmed_{idx + 1:05d}",
            "content": (
                "Question:"
                f" {_safe_str(item.get('instruction') or item.get('question'))}\n\nContext:"
                f" {_safe_str(item.get('input'))}\n\nFindings:"
                f" {_safe_str(item.get('output') or item.get('answer'))}"
            ),
            "metadata": {
                "source": "PubMed",
                "title": _safe_str(
                    item.get("instruction") or item.get("question")
                )[:100]
                or f"PubMed Study {idx + 1}",
                "url": "https://pubmed.ncbi.nlm.nih.gov/",
                "document_type": "article",
                "category": "biomedical_research",
            },
        },
    },
    "medmcqa": {
        "hf_repo": "openlifescienceai/medmcqa",
        "split": "train",
        "source": "ClinicalGuideline",
        "document_type": "guideline",
        "output_file": "medmcqa_dataset.json",
        "builder": lambda item, idx: {
            "document_id": f"medmcqa_{idx + 1:05d}",
            "content": (
                f"Clinical Question: {_safe_str(item.get('question'))}\n\n"
                f"Explanation: {_safe_str(item.get('exp')) or 'No explicit explanation provided.'}"
            ),
            "metadata": {
                "source": "ClinicalGuideline",
                "title": _safe_str(item.get("question"))[:100]
                or f"Clinical Case {idx + 1}",
                "url": None,
                "document_type": "guideline",
                "category": _safe_str(item.get("subject_name")).lower()
                or "clinical medicine",
            },
        },
    },
}


def download_dataset(dataset_key: str, limit: int = 50) -> Path:
  """Streams and transforms a single registered dataset."""
  if dataset_key not in DATASET_REGISTRY:
    raise ValueError(
        f"Unknown dataset '{dataset_key}'. Registered:"
        f" {list(DATASET_REGISTRY.keys())}"
    )

  config = DATASET_REGISTRY[dataset_key]
  print(
      f"Fetching up to {limit} records for '{dataset_key}' from"
      f" {config['hf_repo']}..."
  )

  dataset = load_dataset(config["hf_repo"], split=config["split"], streaming=True)
  builder: Callable[[dict, int], dict] = config["builder"]

  records = []
  for idx, item in enumerate(dataset):
    if idx >= limit:
      break
    records.append(builder(item, idx))

  output_path = RAW_DIR / config["output_file"]
  output_path.write_text(
      json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
  )
  print(f"  [DONE] Saved {len(records)} records to {output_path}")
  return output_path


def main() -> None:
  parser = argparse.ArgumentParser(
      description="Dynamic Healthcare Dataset Downloader"
  )
  parser.add_argument(
      "--dataset",
      type=str,
      default="all",
      choices=["all"] + list(DATASET_REGISTRY.keys()),
      help="Specify a dataset name or 'all' (default: all)",
  )
  parser.add_argument(
      "--limit",
      type=int,
      default=50,
      help="Number of records to download per dataset (default: 50)",
  )
  args = parser.parse_args()

  targets = (
      list(DATASET_REGISTRY.keys()) if args.dataset == "all" else [args.dataset]
  )

  print(f"Starting acquisition for: {targets} (limit={args.limit} each)\n")
  for key in targets:
    download_dataset(key, limit=args.limit)
  print("\nAll requested datasets have been processed into data/raw/!")


if __name__ == "__main__":
  main()