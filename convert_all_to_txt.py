#!/usr/bin/env python3
"""
Convert all PDFs to clean text using pdftotext.
Processes: downloads/, main folder PDFs, nlp_polarization_downloads/
Outputs to: txt_all/
"""

import os
import re
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/maxzhu/Desktop/polarization papers")
OUTPUT_DIR = BASE_DIR / "txt_all"
OUTPUT_DIR.mkdir(exist_ok=True)

# Source directories and their PDFs
sources = [
    BASE_DIR / "downloads",
    BASE_DIR,  # Main folder PDFs
    BASE_DIR / "nlp_polarization_downloads",
]


def pdf_to_text(pdf_path):
    """Convert PDF to text using pdftotext."""
    try:
        result = subprocess.run(
            ['pdftotext', '-layout', str(pdf_path), '-'],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return result.stdout
    except subprocess.TimeoutExpired:
        pass
    except Exception as e:
        print(f"  pdftotext error: {e}")

    # Fallback: try without -layout
    try:
        result = subprocess.run(
            ['pdftotext', str(pdf_path), '-'],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return result.stdout
    except:
        pass

    return None


def clean_text(text):
    """Clean extracted text."""
    if not text:
        return ""

    # Remove form feed characters
    text = text.replace('\f', '\n\n')

    # Remove excessive blank lines (more than 2 in a row)
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # Remove lines that are just page numbers
    text = re.sub(r'\n\s*\d{1,3}\s*\n', '\n', text)

    # Remove common header/footer patterns
    # e.g., "Downloaded from..." lines
    text = re.sub(r'Downloaded from .+\n', '', text)
    text = re.sub(r'This content downloaded from .+\n', '', text)

    # Fix hyphenation at line breaks (word- \n continuation)
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)

    # Strip trailing whitespace from each line
    lines = text.split('\n')
    lines = [line.rstrip() for line in lines]
    text = '\n'.join(lines)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def process_all():
    """Process all PDFs from all sources."""
    processed = 0
    skipped = 0
    failed = 0

    all_pdfs = []
    for source_dir in sources:
        if not source_dir.exists():
            continue
        for pdf_file in sorted(source_dir.glob("*.pdf")):
            all_pdfs.append(pdf_file)

    print(f"Found {len(all_pdfs)} PDFs to process")

    for pdf_file in all_pdfs:
        # Output filename: same as PDF but .txt
        txt_filename = pdf_file.stem + '.txt'
        txt_path = OUTPUT_DIR / txt_filename

        # Skip if already converted
        if txt_path.exists() and txt_path.stat().st_size > 100:
            skipped += 1
            continue

        print(f"  Converting: {pdf_file.name[:70]}...", end=" ")

        raw_text = pdf_to_text(pdf_file)
        if raw_text and len(raw_text) > 200:
            cleaned = clean_text(raw_text)
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            size_kb = len(cleaned) / 1024
            print(f"OK ({size_kb:.0f} KB)")
            processed += 1
        else:
            print("FAILED (no text extracted)")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Processed: {processed}")
    print(f"Skipped (already done): {skipped}")
    print(f"Failed: {failed}")
    print(f"Total in {OUTPUT_DIR}: {len(list(OUTPUT_DIR.glob('*.txt')))}")


if __name__ == '__main__':
    process_all()
