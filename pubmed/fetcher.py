from typing import List, Dict
import xmltodict
import requests
import logging

def fetch_pubmed_ids(query: str, max_results: int = 20) -> List[str]:
    logging.debug(f"Searching PubMed for: {query}")
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]

def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    articles = xmltodict.parse(response.content)["PubmedArticleSet"]["PubmedArticle"]
    if isinstance(articles, dict):
        articles = [articles]
    return articles

