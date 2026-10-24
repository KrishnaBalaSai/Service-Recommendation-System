# evaluation/run_evaluation.py

from evaluation.metrics import precision_at_k, recall_at_k
from evaluation.test_data import test_cases

# This should call your ACTUAL pipeline
from app import get_recommendations   # or system_fn

def evaluate(system_fn, test_cases):
    scores = []

    for case in test_cases:
        results = system_fn(case["query"])
        p = precision_at_k(results, case["relevant_items"])
        r = recall_at_k(results, case["relevant_items"])
        scores.append((p, r))

    avg_p = sum(s[0] for s in scores) / len(scores)
    avg_r = sum(s[1] for s in scores) / len(scores)

    return avg_p, avg_r


if __name__ == "__main__":
    p, r = evaluate(get_recommendations, test_cases)
    print("Precision@5:", p)
    print("Recall@5:", r)
