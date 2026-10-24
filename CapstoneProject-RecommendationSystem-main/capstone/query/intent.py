# query/intent.py
import re

def detect_intent(query: str):
    q = query.lower()

    wants_book = any(x in q for x in ["book", "novel", "read", "fantasy", "thriller"])
    wants_service = any(x in q for x in ["cloud", "deploy", "ml", "api", "hosting"])

    if wants_book and wants_service:
        return "hybrid"
    if wants_book:
        return "book"
    if wants_service:
        return "service"
    return "unknown"

def extract_budget(query: str):
    match = re.search(r"(\d{3,6})", query)
    return int(match.group(1)) if match else None
