def explain_book(book, query, prefs, budget):
    reasons = []

    reasons.append("Semantically relevant to your query")

    if budget and book.get("price_inr", 0) <= budget:
        reasons.append("Fits within your budget")

    if any(p in book.get("title", "").lower() for p in prefs):
        reasons.append("Matches your past reading interests")

    if book.get("average_rating", 0) >= 4:
        reasons.append("Highly rated by readers")

    return reasons


def explain_service(service, query, prefs, budget):
    reasons = []

    reasons.append("Relevant to ML / developer workflow")

    price = service.get("pricing", {}).get("monthly_cost_inr")

    if price is not None and budget and price <= budget:
        reasons.append("Cost-effective under your budget")

    if service.get("provider", "").lower() in prefs:
        reasons.append("Matches your preferred cloud providers")

    if service.get("pricing", {}).get("is_free_tier"):
        reasons.append("Has a free tier available")

    return reasons
