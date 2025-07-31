import requests
import xmltodict
from typing import List, Dict

def fetch_pubmed_ids(query: str) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "retmode": "xml", "retmax": "20", "term": query}
    response = requests.get(url, params=params)
    data = xmltodict.parse(response.text)
    return data["eSearchResult"]["IdList"]["Id"]

def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "retmode": "xml", "id": ",".join(pubmed_ids)}
    response = requests.get(url, params=params)
    return xmltodict.parse(response.text)["PubmedArticleSet"]["PubmedArticle"]
