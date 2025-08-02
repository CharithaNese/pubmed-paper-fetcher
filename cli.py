import argparse
import logging
import pandas as pd
from pubmed.fetcher import fetch_pubmed_ids, fetch_details
from pubmed.filters import extract_non_academic_authors

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument("query", help="Search query for PubMed")
    parser.add_argument("-f", "--file", default="results.csv", help="Output CSV filename")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format='[%(levelname)s] %(message)s')

    try:
        pubmed_ids = fetch_pubmed_ids(args.query)
        logging.debug(f"Found {len(pubmed_ids)} PubMed IDs")

        articles = fetch_details(pubmed_ids)
        logging.debug(f"Retrieved {len(articles)} full article records")

        all_authors = []
        for i, article in enumerate(articles):
            try:
                authors = extract_non_academic_authors(article)
                all_authors.extend(authors)
            except Exception as e:
                logging.error(f"Failed to process article: {i}\n{e}")

        logging.debug(f"Filtered down to {len(all_authors)} non-academic author records")
        df = pd.DataFrame(all_authors)
        df.to_csv(args.file, index=False)
        logging.debug(f"Saved {len(all_authors)} records to {args.file}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
