from pathlib import Path
import PyPDF2


def extract_text_from_pdf(pdf_path: Path) -> str:
    text_parts = []

    with pdf_path.open("rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)

    return "\n".join(text_parts).strip()


def save_text(text: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")