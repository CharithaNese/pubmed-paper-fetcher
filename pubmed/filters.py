# pubmed/filters.py
import re
from typing import List, Dict, Any


COMPANY_KEYWORDS = [
    "inc", "ltd", "llc", "gmbh", "corp", "co.", "company", "biotech", "pharma",
    "therapeutics", "laboratories", "sciences", "diagnostics", "novartis",
    "pfizer", "astrazeneca", "regeneron", "genentech", "moderna", "sanofi",
    "abbvie", "merck", "bayer", "gilead", "roche", "johnson & johnson", "takeda"
]

def is_non_academic(affiliation: str) -> bool:
    affiliation = affiliation.lower()
    return any(keyword in affiliation for keyword in COMPANY_KEYWORDS)

def extract_non_academic_authors(article: Dict[str, Any]) -> List[Dict[str, str]]:
    try:
        authors = article.get("MedlineCitation", {}).get("Article", {}).get("AuthorList", {}).get("Author", [])
        if not isinstance(authors, list):
            authors = [authors]
    except Exception:
        return []

    non_academics = []

    for author in authors:
        try:
            name = f"{author.get('ForeName', '')} {author.get('LastName', '')}".strip()
            aff_info = author.get("AffiliationInfo", [])
            if not isinstance(aff_info, list):
                aff_info = [aff_info]
            affiliations = [a.get("Affiliation", "") for a in aff_info if isinstance(a, dict)]

            for aff in affiliations:
                if is_non_academic(aff):
                    non_academics.append({
                        "Name": name,
                        "Affiliation": aff
                    })
                    break
        except Exception:
            continue

    return non_academics
