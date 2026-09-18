from pathlib import Path
import re

TXT_DIR = Path("literature/txt")
OUTPUT = Path("literature/monster_abstract.txt")
missing_files = []

def extract_abstract(text):
    """
    Extract abstract from common academic-paper formats.

    Handles things like:
        ABSTRACT
        Abstract
        a b s t r a c t
        A B S T R A C T
        Abstract—
    """

    # ABSTRACT / A B S T R A C T / a b s t r a c t
    abstract_header = (
        r"(?:abstract|"
        r"a\s*b\s*s\s*t\s*r\s*a\s*c\s*t)"
    )

    # KEYWORDS / K E Y W O R D S
    keywords_header = (
        r"(?:keywords?|"
        r"k\s*e\s*y\s*w\s*o\s*r\s*d\s*s?)"
    )

    # INDEX TERMS / I N D E X  T E R M S
    index_terms_header = (
        r"(?:index\s*terms?|"
        r"i\s*n\s*d\s*e\s*x\s+"
        r"t\s*e\s*r\s*m\s*s?)"
    )

    # INTRODUCTION / I N T R O D U C T I O N
    introduction_header = (
        r"(?:introduction|"
        r"i\s*n\s*t\s*r\s*o\s*d\s*u\s*c\s*t\s*i\s*o\s*n)"
    )

    pattern = rf"""
        \b{abstract_header}\b
        [\s:\-—–\.]*

        (.*?)

        (?=
            \b{keywords_header}\b
            |
            \b{index_terms_header}\b
            |
            \b(?:I\.|1\.?)?\s*{introduction_header}\b
        )
    """

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE | re.DOTALL | re.VERBOSE
    )

    if match:
        abstract = match.group(1).strip()

        if 50 < len(abstract) < 10000:
            return abstract

    return "[ABSTRACT NOT FOUND AUTOMATICALLY]"

txt_files = sorted(TXT_DIR.glob("*.txt"))

print(f"Found {len(txt_files)} TXT files.\n")

found = 0
missing = 0

with OUTPUT.open("w", encoding="utf-8") as out:

    for i, txt_path in enumerate(txt_files, start=1):

        text = txt_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        abstract = extract_abstract(text)

        if abstract == "[ABSTRACT NOT FOUND AUTOMATICALLY]":
            missing += 1
            missing_files.append(txt_path.name)
            status = "NOT FOUND"
        else:
            found += 1
            status = "FOUND"

        print(
            f"[{i}/{len(txt_files)}] "
            f"{status}: {txt_path.name}"
        )

        out.write("=" * 100 + "\n")
        out.write(f"PAPER: {txt_path.stem}\n")
        out.write(f"FILE: {txt_path.name}\n")
        out.write("=" * 100 + "\n\n")

        out.write("ABSTRACT:\n\n")
        out.write(abstract)

        out.write("\n\n\n")


print("\nFinished!")
print(f"Abstracts found: {found}")
print(f"Abstracts not found: {missing}")
print(f"\nCreated: {OUTPUT}")

if missing_files:
    print("\nFiles with missing abstracts:")
    for filename in missing_files:
        print(f"  - {filename}")