import typer
import pandas as pd
from pubmed.fetcher import fetch_pubmed_ids, fetch_details
from pubmed.filters import extract_data

app = typer.Typer()

@app.command()
def main(query: str,
         file: str = typer.Option(None, "-f", "--file", help="Output file"),
         debug: bool = typer.Option(False, "-d", "--debug"),
         help_flag: bool = typer.Option(False, "-h", "--help", is_eager=True)):

    if help_flag:
        typer.echo("Usage: get-papers-list 'query' [-f file.csv] [-d]")
        raise typer.Exit()

    if debug:
        typer.echo(f"Searching PubMed for: {query}")

    ids = fetch_pubmed_ids(query)
    articles = fetch_details(ids)

    records = [extract_data(a) for a in articles if extract_data(a)]

    df = pd.DataFrame(records)
    if file:
        df.to_csv(file, index=False)
    else:
        typer.echo(df.to_string(index=False))

if __name__ == "__main__":
    app()
