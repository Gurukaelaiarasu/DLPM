import argparse
import os
import csv
from typing import List

import pandas as pd
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
import requests


def parse_url(url: str) -> pd.DataFrame:
    """Fetch tables from an HTML page."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as exc:
        print(f"Failed to fetch {url}: {exc}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    dfs = []
    for table in tables:
        try:
            dfs.append(pd.read_html(str(table))[0])
        except ValueError:
            continue
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return pd.DataFrame()


def parse_pdf(path: str) -> pd.DataFrame:
    """Attempt to parse comma separated tables from a PDF."""
    try:
        text = extract_text(path)
    except Exception as exc:
        print(f"Failed to read {path}: {exc}")
        return pd.DataFrame()

    lines = [line.strip() for line in text.splitlines() if "," in line]
    if not lines:
        return pd.DataFrame()
    reader = csv.reader(lines)
    rows = list(reader)
    df = pd.DataFrame(rows)
    # assume first row is header
    if len(df) > 1:
        df.columns = df.iloc[0]
        df = df.drop(0).reset_index(drop=True)
    return df


def main(urls: List[str], pdfs: List[str], output: str) -> None:
    dfs = []
    for url in urls:
        dfs.append(parse_url(url))
    for pdf in pdfs:
        if os.path.exists(pdf):
            dfs.append(parse_pdf(pdf))
        else:
            print(f"PDF not found: {pdf}")
    if not dfs:
        print("No data scraped.")
        return
    result = pd.concat(dfs, ignore_index=True)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    result.to_csv(output, index=False)
    print(f"Saved {len(result)} rows to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape thin-film metamaterial data from URLs or PDFs")
    parser.add_argument("--urls", nargs="*", default=[], help="List of URLs containing HTML tables")
    parser.add_argument("--pdfs", nargs="*", default=[], help="List of local PDF files")
    parser.add_argument("--output", default="Datasets/raw/scraped_data.csv", help="Output CSV file")
    args = parser.parse_args()
    main(args.urls, args.pdfs, args.output)
