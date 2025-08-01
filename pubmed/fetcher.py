import requests
import xmltodict
from typing import List, Dict

def fetch_pubmed_ids(query: str) -> List[str]:
    print(f"[DEBUG] Searching PubMed for: {query}")
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "retmode": "xml",
        "retmax": "20",  # Max 20 articles
        "term": query
    }
    response = requests.get(url, params=params)
    data = xmltodict.parse(response.text)

    ids = data["eSearchResult"]["IdList"].get("Id", [])
    if isinstance(ids, str):  # if only 1 ID returned
        ids = [ids]

    print(f"[DEBUG] Found {len(ids)} PubMed IDs")
    return ids

def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    print(f"[DEBUG] Fetching details for {len(pubmed_ids)} articles")
    if not pubmed_ids:
        return []

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "retmode": "xml",
        "id": ",".join(pubmed_ids)
    }
    response = requests.get(url, params=params)
    data = xmltodict.parse(response.text)

    articles = data.get("PubmedArticleSet", {}).get("PubmedArticle", [])
    if isinstance(articles, dict):  # single article case
        articles = [articles]

    print(f"[DEBUG] Retrieved {len(articles)} full article records")
    return articles
