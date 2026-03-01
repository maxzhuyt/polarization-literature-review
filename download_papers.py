#!/usr/bin/env python3
"""
Download full-text PDFs for polarization review articles.
Strategy:
1. Unpaywall API (free, legal open-access copies)
2. UChicago DOI proxy (institutional access)
3. Google Scholar (fallback, manual)
"""

import re
import os
import json
import time
import urllib.parse
import requests
from pathlib import Path

# --- Config ---
BASE_DIR = Path("/Users/maxzhu/Desktop/polarization papers")
DOWNLOAD_DIR = BASE_DIR / "downloads"
TXT_DIR = BASE_DIR / "txt"
NLP_DIR = BASE_DIR / "nlp_polarization_downloads"
LOG_FILE = BASE_DIR / "download_log.json"
UNPAYWALL_EMAIL = "research@uchicago.edu"  # Required by Unpaywall API

DOWNLOAD_DIR.mkdir(exist_ok=True)

# --- Parse the MD file to get unique DOI papers ---
def parse_md():
    with open(BASE_DIR / "polarization_review_articles.md") as f:
        content = f.read()

    papers = {}
    for line in content.split('\n'):
        if not line.startswith('|') or line.startswith('|---') or line.startswith('| #'):
            continue
        doi_match = re.search(r'\[([0-9][0-9]\.[^\]]+)\]\(https://doi\.org/', line)
        if not doi_match:
            continue
        doi = doi_match.group(1)
        if doi in papers:
            continue

        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 5:
            title = re.sub(r'\*+', '', parts[2]).strip()  # Remove markdown italic
            authors = parts[3]
            year = parts[4]
            author_last = authors.split(',')[0].split(';')[0].strip()

            # Generate a clean filename
            safe_author = re.sub(r'[^\w\s-]', '', author_last).strip()
            safe_title = re.sub(r'[^\w\s-]', '', title[:60]).strip()
            filename = f"{safe_author} et al. - {year} - {safe_title}"

            papers[doi] = {
                'doi': doi,
                'title': title,
                'authors': authors,
                'year': year,
                'filename': filename,
            }
    return papers


def already_have(paper):
    """Check if we already have this paper as PDF or txt."""
    author_last = paper['authors'].split(',')[0].split(';')[0].strip().lower()
    year = paper['year']

    # Check txt/ folder
    for f in TXT_DIR.iterdir():
        if author_last in f.name.lower() and year in f.name:
            return True

    # Check main folder PDFs
    for f in BASE_DIR.glob("*.pdf"):
        if author_last in f.name.lower() and year in f.name:
            return True

    # Check downloads/ folder
    for f in DOWNLOAD_DIR.glob("*.pdf"):
        if author_last in f.name.lower() and year in f.name:
            return True

    # Check nlp_polarization_downloads/
    for f in NLP_DIR.glob("*.pdf"):
        if author_last in f.name.lower() and year in f.name:
            return True

    return False


def try_unpaywall(doi):
    """Try to get PDF URL from Unpaywall (legal open access)."""
    url = f"https://api.unpaywall.org/v2/{doi}?email={UNPAYWALL_EMAIL}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            # Try best OA location first
            best = data.get('best_oa_location')
            if best:
                pdf_url = best.get('url_for_pdf') or best.get('url')
                if pdf_url:
                    return pdf_url
            # Try all OA locations
            for loc in data.get('oa_locations', []):
                pdf_url = loc.get('url_for_pdf') or loc.get('url')
                if pdf_url and pdf_url.endswith('.pdf'):
                    return pdf_url
    except Exception as e:
        print(f"  Unpaywall error: {e}")
    return None


def try_doi_proxy(doi):
    """Try to resolve DOI through UChicago proxy and find PDF."""
    proxy_url = f"https://doi-org.proxy.uchicago.edu/{doi}"
    try:
        resp = requests.get(proxy_url, timeout=20, allow_redirects=True,
                          headers={'User-Agent': 'Mozilla/5.0'})
        final_url = resp.url

        # For some publishers, we can construct the PDF URL
        # PNAS
        if 'pnas.org' in final_url:
            pdf_url = final_url.replace('/doi/', '/doi/pdf/')
            return pdf_url
        # Science / Science Advances
        if 'science.org' in final_url:
            pdf_url = final_url.replace('/doi/', '/doi/pdf/')
            return pdf_url
        # Annual Reviews
        if 'annualreviews.org' in final_url:
            pdf_url = final_url.replace('/doi/', '/doi/pdf/')
            return pdf_url
        # Wiley (AJPS etc)
        if 'onlinelibrary.wiley.com' in final_url:
            pdf_url = final_url.replace('/doi/', '/doi/pdfdirect/')
            return pdf_url
        # SAGE
        if 'journals.sagepub.com' in final_url:
            pdf_url = final_url.replace('/doi/', '/doi/pdf/')
            return pdf_url
        # Oxford (POQ, BJPS)
        if 'academic.oup.com' in final_url:
            # OUP PDF pattern: add ?pdf at end
            return final_url
        # Elsevier / ScienceDirect
        if 'sciencedirect.com' in final_url:
            return final_url  # Will need browser for actual download
        # Nature
        if 'nature.com' in final_url:
            if '.pdf' not in final_url:
                pdf_url = final_url + '.pdf'
                return pdf_url
        # Cambridge University Press
        if 'cambridge.org' in final_url:
            pdf_url = final_url.replace('/article/', '/article/pdf/')
            return pdf_url
        # AEA
        if 'aeaweb.org' in final_url:
            return final_url
        # Taylor & Francis
        if 'tandfonline.com' in final_url:
            pdf_url = final_url.replace('/doi/', '/doi/pdf/')
            return pdf_url
        # JSTOR
        if 'jstor.org' in final_url:
            m = re.search(r'/stable/(\d+)', final_url)
            if m:
                return f"https://www.jstor.org/stable/pdf/{m.group(1)}.pdf"

        return final_url  # Return whatever we got
    except Exception as e:
        print(f"  DOI proxy error: {e}")
    return None


def download_pdf(url, filepath):
    """Download a PDF from a URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/pdf,*/*',
        }
        resp = requests.get(url, timeout=30, headers=headers, allow_redirects=True)

        # Check if we got a PDF
        content_type = resp.headers.get('content-type', '')
        if 'pdf' in content_type or resp.content[:4] == b'%PDF':
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            size_kb = len(resp.content) / 1024
            if size_kb < 10:
                os.remove(filepath)
                return False, "Too small, likely not a real PDF"
            return True, f"Downloaded ({size_kb:.0f} KB)"
        else:
            return False, f"Not a PDF (content-type: {content_type[:50]})"
    except Exception as e:
        return False, str(e)


def main():
    papers = parse_md()
    print(f"Total unique DOI papers in MD: {len(papers)}")

    # Filter out papers we already have
    to_download = {}
    already_count = 0
    for doi, paper in papers.items():
        if already_have(paper):
            already_count += 1
        else:
            to_download[doi] = paper

    print(f"Already have: {already_count}")
    print(f"Need to download: {len(to_download)}")
    print()

    # Track results
    results = {'success': [], 'failed': [], 'need_browser': []}

    for i, (doi, paper) in enumerate(to_download.items(), 1):
        print(f"[{i}/{len(to_download)}] {paper['authors'][:30]} ({paper['year']}) - {paper['title'][:50]}...")

        filepath = DOWNLOAD_DIR / f"{paper['filename']}.pdf"

        # Strategy 1: Unpaywall
        print("  Trying Unpaywall...", end=" ")
        pdf_url = try_unpaywall(doi)
        if pdf_url:
            print(f"Found: {pdf_url[:60]}...")
            success, msg = download_pdf(pdf_url, filepath)
            if success:
                print(f"  SUCCESS: {msg}")
                results['success'].append({'doi': doi, 'method': 'unpaywall', **paper})
                time.sleep(0.5)
                continue
            else:
                print(f"  Failed download: {msg}")
        else:
            print("No OA version found")

        # Strategy 2: Direct DOI with publisher PDF patterns
        print("  Trying direct DOI...", end=" ")
        pdf_url = try_doi_proxy(doi)
        if pdf_url:
            print(f"Found: {pdf_url[:60]}...")
            success, msg = download_pdf(pdf_url, filepath)
            if success:
                print(f"  SUCCESS: {msg}")
                results['success'].append({'doi': doi, 'method': 'doi_direct', **paper})
                time.sleep(0.5)
                continue
            else:
                print(f"  Failed download: {msg}")
                results['need_browser'].append({'doi': doi, 'url': pdf_url, **paper})
        else:
            print("Could not resolve")
            results['failed'].append({'doi': doi, **paper})

        time.sleep(1)  # Be polite

    # Summary
    print("\n" + "="*60)
    print(f"RESULTS:")
    print(f"  Downloaded: {len(results['success'])}")
    print(f"  Need browser: {len(results['need_browser'])}")
    print(f"  Failed: {len(results['failed'])}")

    if results['need_browser']:
        print(f"\nPapers that need browser download (institutional access):")
        for p in results['need_browser']:
            print(f"  - {p['doi']}: {p['title'][:60]}")
            print(f"    URL: {p.get('url', 'N/A')}")

    if results['failed']:
        print(f"\nFailed papers:")
        for p in results['failed']:
            print(f"  - {p['doi']}: {p['title'][:60]}")

    # Save log
    with open(LOG_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nLog saved to {LOG_FILE}")


if __name__ == '__main__':
    main()
