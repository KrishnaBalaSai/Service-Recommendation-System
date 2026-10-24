# ranking/reranker.py

import json
from llm.gemini_client import call_gemini

def rerank(query, items, top_n=5):
    """
    items: list of dicts with keys: id, title, description
    """

    prompt = f"""
You are a relevance ranking system.

Query:
{query}

Below are candidate items. Rank them from most relevant to least relevant.
Return ONLY a JSON list of item ids in ranked order.

Items:
"""

    for i, item in enumerate(items, start=1):
        prompt += f"""
{i}. ID: {item['id']}
Title: {item['title']}
Description: {item['description']}
"""

    prompt += "\nReturn format example: [\"id3\", \"id1\", \"id2\"]"

    response = call_gemini(prompt)

    try:
        ranked_ids = json.loads(response)
        return ranked_ids[:top_n]
    except Exception:
        # fallback: no reranking
        return [item["id"] for item in items[:top_n]]
