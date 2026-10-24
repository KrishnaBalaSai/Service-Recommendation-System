# evaluation/metrics.py
def precision_at_k(recommended, relevant, k=5):
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    hits = sum(1 for item in recommended_k if item in relevant_set)
    return hits / k

def recall_at_k(recommended, relevant, k=5):
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    hits = sum(1 for item in recommended_k if item in relevant_set)
    return hits / len(relevant_set) if relevant_set else 0
