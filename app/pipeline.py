import json
from pathlib import Path
from typing import Optional
from .config import CSV_PATH, PDF_DIR, TEXT_DIR, JSON_DIR
from .mitos_client import MitosClient
from .pdf_utils import extract_text_from_pdf, save_text
from .llm_extractor import LLMExtractor


class PreconditionsPipeline:
    def __init__(self):
        self.client = MitosClient()
        self.llm = LLMExtractor()

    def run(self, limit: Optional[int] = None) -> None:
        process_ids = self.client.get_process_ids(CSV_PATH)

        if limit is not None:
            process_ids = process_ids[:limit]

        print(f"Loaded {len(process_ids)} process IDs")

        for process_id in process_ids:
            print(f"\nProcessing service {process_id}")

            try:
                service = self.client.fetch_service(process_id)
            except Exception as e:
                print(f"Failed to fetch service {process_id}: {e}")
                continue

            # Save API conditions directly too
            api_conditions_path = JSON_DIR / f"{process_id}_api_conditions.json"
            api_conditions = {
                "process_id": process_id,
                "conditions": [c.condition_name for c in service.conditions],
            }
            api_conditions_path.write_text(
                json.dumps(api_conditions, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )

            # Download PDFs
            for idx, rule in enumerate(service.rules):
                pdf_path = PDF_DIR / process_id / f"rule_{idx}.pdf"
                ok = self.client.download_file(rule.rule_url, pdf_path)
                if not ok:
                    print(f"Failed to download {rule.rule_url}")
                    continue

                # Extract raw text
                try:
                    text = extract_text_from_pdf(pdf_path)
                except Exception as e:
                    print(f"Failed to parse PDF {pdf_path.name}: {e}")
                    continue

                if not text.strip():
                    print(f"No text extracted from {pdf_path.name}")
                    continue

                text_path = TEXT_DIR / process_id / f"rule_{idx}.txt"
                save_text(text, text_path)

                # LLM extraction
                try:
                    result = self.llm.extract_preconditions(process_id, text)
                    output_path = JSON_DIR / process_id / f"rule_{idx}_llm.json"
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_text(
                        json.dumps(result, ensure_ascii=False, indent=2),
                        encoding="utf-8"
                    )
                    print(f"Saved structured output: {output_path}")
                except Exception as e:
                    print(f"LLM extraction failed for {process_id}, file {pdf_path.name}: {e}")