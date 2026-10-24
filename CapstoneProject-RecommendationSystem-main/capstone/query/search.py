# query/search.py
from db import db
from config import BOOKS_COLLECTION, SERVICES_COLLECTION

def search_books(vector, budget=None, k=5):
    stage = {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": vector,
            "numCandidates": 150,
            "limit": k
        }
    }

    if budget:
        stage["$vectorSearch"]["filter"] = {"price_inr": {"$lte": budget}}

    return list(db[BOOKS_COLLECTION].aggregate([
        stage,
        {"$project": {
            "_id": 1,
            "title": 1,
            "authors": 1,
            "price_inr": 1,
            "average_rating": 1
        }}

    ]))

def search_services(vector, budget=None, k=5):
    results = list(db[SERVICES_COLLECTION].aggregate([
        {
            "$vectorSearch": {
                "index": "services_vector_index",
                "path": "embedding",
                "queryVector": vector,
                "numCandidates": 300,
                "limit": 20
            }
        },
        {"$project": {
            "_id": 1,
            "service_name": 1,
            "provider": 1,
            "pricing": 1
        }}

    ]))

    filtered = []
    for s in results:
        price = s.get("pricing", {}).get("monthly_cost_inr")
        if budget is None or price is None or price <= budget:
            filtered.append(s)

    return filtered[:k]
