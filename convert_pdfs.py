from pathlib import Path
import fitz

PDF_DIR = Path("literature/pdfs")
TXT_DIR = Path("literature/txt")

TXT_DIR.mkdir(parents=True, exist_ok=True)

pdf_files = list(PDF_DIR.glob("*.pdf"))

print(f"Found {len(pdf_files)} PDF files.\n")

for i, pdf_path in enumerate(pdf_files, start=1):

    txt_path = TXT_DIR / f"{pdf_path.stem}.txt"

    print(f"[{i}/{len(pdf_files)}] {pdf_path.name}")

    try:
        document = fitz.open(pdf_path)

        text_parts = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text()

            text_parts.append(
                f"\n\n--- PAGE {page_number} ---\n\n{text}"
            )

        full_text = "".join(text_parts)

        txt_path.write_text(
            full_text,
            encoding="utf-8",
            errors="ignore"
        )

        document.close()

        print(f"    -> {txt_path}")

    except Exception as e:
        print(f"    ERROR: {e}")


print("\nFinished!")