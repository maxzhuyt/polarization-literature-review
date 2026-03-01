#!/usr/bin/env python3
"""
Download papers via UChicago EZProxy using cookies from the browser session.
Two strategies:
1. Google Scholar search → extract PDF URL → convert to proxy URL → download
2. Direct DOI → publisher-specific PDF URL patterns → proxy URL → download
"""

import re
import os
import json
import time
import urllib.parse
import requests
from pathlib import Path

BASE_DIR = Path("/Users/maxzhu/Desktop/polarization papers")
DOWNLOAD_DIR = BASE_DIR / "downloads"
LOG_FILE = BASE_DIR / "download_log.json"

DOWNLOAD_DIR.mkdir(exist_ok=True)

# EZProxy cookie from browser session
EZPROXY_COOKIE = "OMmaS6LheZIuBG4"

def get_session():
    """Create a requests session with proxy cookies and browser-like headers."""
    s = requests.Session()
    s.cookies.set("ezproxy", EZPROXY_COOKIE, domain=".uchicago.edu", path="/")
    s.cookies.set("ezproxyl", EZPROXY_COOKIE, domain=".uchicago.edu", path="/")
    s.cookies.set("ezproxyn", EZPROXY_COOKIE, domain=".uchicago.edu", path="/")
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8',
    })
    return s


def to_proxy_url(url):
    """Convert a regular URL to a UChicago proxy URL."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    # e.g., academic.oup.com → academic-oup-com.proxy.uchicago.edu
    proxy_host = parsed.hostname.replace('.', '-') + '.proxy.uchicago.edu'
    proxy_url = f"{parsed.scheme}://{proxy_host}{parsed.path}"
    if parsed.query:
        proxy_url += f"?{parsed.query}"
    return proxy_url


def doi_to_pdf_urls(doi):
    """Generate candidate PDF URLs based on DOI prefix (publisher-specific patterns)."""
    urls = []

    # Annual Reviews (10.1146/)
    if doi.startswith('10.1146/'):
        urls.append(f'https://www.annualreviews.org/doi/pdf/{doi}')

    # OUP - Oxford (10.1093/)
    elif doi.startswith('10.1093/'):
        # Need to resolve DOI first to get the article path
        urls.append(f'https://doi.org/{doi}')  # Will resolve

    # Nature group (10.1038/)
    elif doi.startswith('10.1038/'):
        # Nature articles: https://www.nature.com/articles/ID.pdf
        article_id = doi.split('/')[-1]
        urls.append(f'https://www.nature.com/articles/{article_id}.pdf')

    # Science/AAAS (10.1126/)
    elif doi.startswith('10.1126/'):
        urls.append(f'https://www.science.org/doi/pdf/{doi}')

    # Wiley (10.1111/)
    elif doi.startswith('10.1111/'):
        urls.append(f'https://onlinelibrary.wiley.com/doi/pdfdirect/{doi}')

    # UChicago Press (10.1086/)
    elif doi.startswith('10.1086/'):
        urls.append(f'https://www.journals.uchicago.edu/doi/pdf/{doi}')

    # SAGE (10.1177/)
    elif doi.startswith('10.1177/'):
        urls.append(f'https://journals.sagepub.com/doi/pdf/{doi}')

    # Elsevier (10.1016/)
    elif doi.startswith('10.1016/'):
        # ScienceDirect doesn't have simple PDF URLs, need to resolve
        urls.append(f'https://doi.org/{doi}')

    # Cambridge UP (10.1017/)
    elif doi.startswith('10.1017/'):
        urls.append(f'https://doi.org/{doi}')

    # PNAS (10.1073/)
    elif doi.startswith('10.1073/'):
        urls.append(f'https://www.pnas.org/doi/pdf/{doi}')

    # APA (10.1037/)
    elif doi.startswith('10.1037/'):
        urls.append(f'https://doi.org/{doi}')

    # Taylor & Francis (10.1080/)
    elif doi.startswith('10.1080/'):
        urls.append(f'https://www.tandfonline.com/doi/pdf/{doi}')

    # AEA (10.1257/)
    elif doi.startswith('10.1257/'):
        urls.append(f'https://www.aeaweb.org/articles/pdf/doi/{doi}')

    # JSTOR (10.2307/)
    elif doi.startswith('10.2307/'):
        jstor_id = doi.replace('10.2307/', '')
        urls.append(f'https://www.jstor.org/stable/pdf/{jstor_id}.pdf')

    # PhysRev (10.1103/)
    elif doi.startswith('10.1103/'):
        urls.append(f'https://journals.aps.org/prl/pdf/{doi}')

    # Review of Economics and Statistics (10.1162/)
    elif doi.startswith('10.1162/'):
        urls.append(f'https://direct.mit.edu/rest/article-pdf/doi/{doi}')

    # Econometrica (10.3982/)
    elif doi.startswith('10.3982/'):
        urls.append(f'https://onlinelibrary.wiley.com/doi/pdfdirect/{doi}')

    # Generic fallback
    else:
        urls.append(f'https://doi.org/{doi}')

    return urls


def try_download_pdf(session, url, filepath, use_proxy=True):
    """Try to download a PDF from a URL, optionally through the proxy."""
    try:
        if use_proxy:
            dl_url = to_proxy_url(url)
        else:
            dl_url = url

        resp = session.get(dl_url, timeout=30, allow_redirects=True)

        content_type = resp.headers.get('content-type', '')

        # Check if we got a PDF
        if resp.status_code == 200 and (resp.content[:4] == b'%PDF' or 'pdf' in content_type):
            size = len(resp.content)
            if size > 10000:  # At least 10KB
                with open(filepath, 'wb') as f:
                    f.write(resp.content)
                return True, f"Downloaded ({size // 1024} KB)"
            return False, f"Too small ({size} bytes)"

        # If we got HTML, try to find a PDF link in it
        if resp.status_code == 200 and 'html' in content_type:
            # Look for PDF links in the page
            pdf_links = re.findall(r'href=["\']([^"\']*?\.pdf[^"\']*?)["\']', resp.text)
            if pdf_links:
                for pdf_link in pdf_links[:3]:
                    if not pdf_link.startswith('http'):
                        from urllib.parse import urljoin
                        pdf_link = urljoin(dl_url, pdf_link)
                    # Try downloading the PDF link
                    if use_proxy:
                        pdf_dl_url = to_proxy_url(pdf_link) if 'proxy.uchicago.edu' not in pdf_link else pdf_link
                    else:
                        pdf_dl_url = pdf_link
                    try:
                        pdf_resp = session.get(pdf_dl_url, timeout=30, allow_redirects=True)
                        if pdf_resp.content[:4] == b'%PDF' and len(pdf_resp.content) > 10000:
                            with open(filepath, 'wb') as f:
                                f.write(pdf_resp.content)
                            return True, f"Downloaded via HTML link ({len(pdf_resp.content) // 1024} KB)"
                    except:
                        continue

        return False, f"Status {resp.status_code}, content-type: {content_type[:50]}"
    except Exception as e:
        return False, str(e)[:100]


def search_google_scholar(session, title, author_last, year):
    """Search Google Scholar and extract PDF URL."""
    query = f'"{title[:80]}" {author_last} {year}'
    params = {
        'q': query,
        'hl': 'en',
        'as_sdt': '0,14',
    }
    try:
        resp = session.get('https://scholar.google.com/scholar', params=params, timeout=15)
        if resp.status_code == 200:
            # Look for PDF links in the results
            # Pattern: href="URL" that leads to a PDF
            pdf_matches = re.findall(r'href="(https?://[^"]+\.pdf[^"]*)"', resp.text)
            if pdf_matches:
                return pdf_matches[0]
            # Also look for links with [PDF] label
            pdf_label_matches = re.findall(r'<a href="(https?://[^"]+)"[^>]*>\[PDF\]', resp.text)
            if pdf_label_matches:
                return pdf_label_matches[0]
        elif resp.status_code == 429:
            print("  Google Scholar rate limited!")
            return None
    except Exception as e:
        print(f"  Scholar error: {e}")
    return None


def get_papers_to_download():
    """Parse the download log to get papers that still need downloading."""
    with open(LOG_FILE) as f:
        log = json.load(f)
    return log.get('need_browser', [])


def already_downloaded(paper):
    """Check if we already have this paper."""
    author_last = paper.get('authors', '').split(',')[0].split(';')[0].strip().lower()
    year = paper.get('year', '')

    for d in [DOWNLOAD_DIR, BASE_DIR, BASE_DIR / 'txt', BASE_DIR / 'nlp_polarization_downloads']:
        if not d.exists():
            continue
        for f in d.iterdir():
            if author_last and author_last in f.name.lower() and year in f.name:
                return True
    return False


def main():
    session = get_session()

    # Test proxy connection
    print("Testing proxy connection...")
    try:
        resp = session.get('https://login.proxy.uchicago.edu/menu', timeout=10)
        if resp.status_code == 200:
            print("  Proxy session active!")
        else:
            print(f"  Warning: proxy returned {resp.status_code}")
    except Exception as e:
        print(f"  Proxy error: {e}")

    # Get papers to download
    papers = get_papers_to_download()
    print(f"\nPapers to download: {len(papers)}")

    # Filter out already downloaded
    to_download = [p for p in papers if not already_downloaded(p)]
    print(f"After filtering already downloaded: {len(to_download)}")

    results = {'downloaded': [], 'failed': []}

    for i, paper in enumerate(to_download, 1):
        doi = paper['doi']
        title = paper.get('title', '')
        authors = paper.get('authors', '')
        year = paper.get('year', '')
        author_last = authors.split(',')[0].split(';')[0].strip()
        filename = paper.get('filename', f"{author_last} et al - {year}")

        filepath = DOWNLOAD_DIR / f"{filename}.pdf"
        if filepath.exists():
            print(f"[{i}/{len(to_download)}] SKIP (exists): {author_last} ({year})")
            continue

        print(f"\n[{i}/{len(to_download)}] {author_last} ({year}) - {title[:50]}...")

        # Strategy 1: Direct publisher PDF URL via proxy
        pdf_urls = doi_to_pdf_urls(doi)
        downloaded = False

        for url in pdf_urls:
            print(f"  Trying: {url[:60]}...")
            success, msg = try_download_pdf(session, url, filepath, use_proxy=True)
            if success:
                print(f"  SUCCESS: {msg}")
                results['downloaded'].append({**paper, 'method': 'direct_proxy'})
                downloaded = True
                break
            else:
                print(f"  Failed: {msg}")

        if not downloaded:
            # Strategy 2: Google Scholar
            print(f"  Trying Google Scholar...")
            gs_url = search_google_scholar(session, title, author_last, year)
            if gs_url:
                print(f"  Found: {gs_url[:60]}...")
                # Try without proxy first (might be OA)
                success, msg = try_download_pdf(session, gs_url, filepath, use_proxy=False)
                if success:
                    print(f"  SUCCESS (OA): {msg}")
                    results['downloaded'].append({**paper, 'method': 'scholar_oa'})
                    downloaded = True
                else:
                    # Try with proxy
                    success, msg = try_download_pdf(session, gs_url, filepath, use_proxy=True)
                    if success:
                        print(f"  SUCCESS (proxy): {msg}")
                        results['downloaded'].append({**paper, 'method': 'scholar_proxy'})
                        downloaded = True
                    else:
                        print(f"  Failed: {msg}")

        if not downloaded:
            results['failed'].append(paper)
            print(f"  FAILED - all strategies exhausted")

        time.sleep(2)  # Be polite

    print(f"\n{'='*60}")
    print(f"Downloaded: {len(results['downloaded'])}")
    print(f"Failed: {len(results['failed'])}")

    if results['failed']:
        print(f"\nStill need:")
        for p in results['failed']:
            print(f"  - {p['doi']}: {p.get('title', '')[:60]}")

    # Save updated log
    with open(BASE_DIR / 'download_log2.json', 'w') as f:
        json.dump(results, f, indent=2)


if __name__ == '__main__':
    main()
