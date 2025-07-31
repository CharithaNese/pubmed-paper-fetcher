from typing import Dict, Optional, List
import re

def is_non_academic(aff: str) -> bool:
    academic_keywords = ["university", "college", "institute", "school", "hospital", "lab", "center"]
    return not any(word.lower() in aff.lower() for word in academic_keywords)

def extract_data(article: Dict) -> Optional[Dict]:
    try:
        pmid = article["MedlineCitation"]["PMID"]["#text"]
        article_data = article["MedlineCitation"]["Article"]
        title = article_data["ArticleTitle"]
        date = article_data.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {}).get("Year", "N/A")
        authors = article_data.get("AuthorList", {}).get("Author", [])

        if not isinstance(authors, list):
            authors = [authors]

        non_academic_authors = []
        companies = []
        email = ""

        for author in authors:
            aff = author.get("AffiliationInfo", [{}])[0].get("Affiliation", "")
            if is_non_academic(aff):
                name = author.get("LastName", "") + ", " + author.get("ForeName", "")
                non_academic_authors.append(name)
                companies.append(aff)

                email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", aff)
                if email_match:
                    email = email_match.group()

        if non_academic_authors:
            return {
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": date,
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(companies),
                "Corresponding Author Email": email,
            }

    except Exception:
        return None
