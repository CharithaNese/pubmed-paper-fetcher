# cli.py

import typer
import pandas as pd
from pubmed.fetcher import fetch_pubmed_ids, fetch_details
from pubmed.filters import extract_non_academic_authors

app = typer.Typer()

@app.command()
def main(
    query: str,
    file: str = typer.Option(None, "-f", "--file", help="Output file"),
    debug: bool = typer.Option(False, "-d", "--debug"),
    help_flag: bool = typer.Option(False, "-h", "--help", is_eager=True)
):
    if help_flag:
        typer.echo("Usage: get-papers-list 'query' [-f file.csv] [-d]")
        raise typer.Exit()

    if debug:
        typer.echo(f"[DEBUG] Searching PubMed for: {query}")

    ids = fetch_pubmed_ids(query)

    if debug:
        typer.echo(f"[DEBUG] Found {len(ids)} PubMed IDs")

    articles = fetch_details(ids)

    if debug:
        typer.echo(f"[DEBUG] Retrieved {len(articles)} full article records")

    results = []
    for article in articles:
        try:
            pmid = article["MedlineCitation"]["PMID"]["#text"]
            title = article["MedlineCitation"]["Article"]["ArticleTitle"]
            date = article["MedlineCitation"]["Article"].get("Journal", {}).get("JournalIssue", {}).get("PubDate", {}).get("Year", "N/A")
            non_acads = extract_non_academic_authors(article)

            for person in non_acads:
                results.append({
                    "PubmedID": pmid,
                    "Title": title,
                    "Publication Date": date,
                    "Non-academic Author(s)": person["Name"],
                    "Company Affiliation(s)": person["Affiliation"],
                })
        except Exception as e:
            if debug:
                typer.echo(f"[ERROR] Failed to process article: {e}")
            continue

    if debug:
        typer.echo(f"[DEBUG] Filtered down to {len(results)} non-academic articles")

    df = pd.DataFrame(results)
    if file:
        try:
            df.to_csv(file, index=False)
            if debug:
                typer.echo(f"[DEBUG] Saved {len(results)} records to {file}")
        except PermissionError:
            typer.echo("[ERROR] Cannot write to file — it may be open in Excel. Close it and try again.")
    else:
        typer.echo(df.to_string(index=False))


if __name__ == "__main__":
    app()

