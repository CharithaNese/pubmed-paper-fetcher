import re
from typing import List, Dict

NON_ACADEMIC_KEYWORDS = [
    "pharma", "biotech", "inc", "ltd", "gmbh", "corp", "co.", "llc", "pvt", "ag", "industries"
]

def is_non_academic_affiliation(affiliation: str) -> bool:
    affiliation_lower = affiliation.lower()
    return any(keyword in affiliation_lower for keyword in NON_ACADEMIC_KEYWORDS)

def extract_email(affiliation: str) -> str:
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", affiliation)
    return match.group(0) if match else ""

def extract_non_academic_authors(article: Dict) -> List[Dict]:
    result = []
    try:
        medline = article.get("MedlineCitation", {})
        article_info = medline.get("Article", {})
        authors = article_info.get("AuthorList", {}).get("Author", [])
        if isinstance(authors, dict):
            authors = [authors]

        for author in authors:
            if not isinstance(author, dict):
                continue

            affiliation_info = author.get("AffiliationInfo")
            if affiliation_info:
                if isinstance(affiliation_info, list):
                    affil_text = affiliation_info[0].get("Affiliation", "")
                else:
                    affil_text = affiliation_info.get("Affiliation", "")
            else:
                affil_text = ""

            if is_non_academic_affiliation(affil_text):
                email = extract_email(affil_text)
                name = f"{author.get('ForeName', '')} {author.get('LastName', '')}".strip()
                result.append({
                    "Author": name,
                    "Affiliation": affil_text,
                    "Email": email
                })
    except Exception as e:
        raise RuntimeError(f"Failed to parse article: {e}")
    return result

