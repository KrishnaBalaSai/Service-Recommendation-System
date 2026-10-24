# rag/context_builder.py

def build_context(books, services):
    if not books and not services:
        #return None, "advisory"
        return None, "advisory"


    context = ""

    if books:
        context += "BOOK RESULTS:\n"
        for b in books:
            context += (
                f"- Title: {b['title']}\n"
                f"  Price: ₹{b['price_inr']}\n"
                f"  Rating: {b.get('average_rating', 'N/A')}\n\n"
            )

    if services:
        context += "SERVICE RESULTS:\n"
        for s in services:
            price = s.get("pricing", {}).get("monthly_cost_inr", "N/A")
            context += (
                f"- Service: {s['service_name']}\n"
                f"  Provider: {s['provider']}\n"
                f"  Monthly Cost: ₹{price}\n\n"
            )

    return context, "grounded"
