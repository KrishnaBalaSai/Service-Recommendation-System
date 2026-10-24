'''# query/vector_selector.py

import numpy as np

def blend_vectors(v_query, v_user, alpha=0.6):
    """
    alpha controls balance:
    0.6 → slightly intent-focused
    0.4 → personalization
    """
    vq = np.array(v_query)
    vu = np.array(v_user)
    return (alpha * vq + (1 - alpha) * vu).tolist()

def select_search_vector(
    intent,
    query_vector,
    user_profile
):
    """
    user_profile: dict or None
    """
    if not user_profile or not user_profile.get("preference_vector"):
        return query_vector, "query_only"

    if intent == "hybrid":
        blended = blend_vectors(
            query_vector,
            user_profile["preference_vector"]
        )
        return blended, "hybrid_blend"

    if user_profile.get("num_likes", 0) >= 3:
        return user_profile["preference_vector"], "user_only"

    return query_vector, "query_only"
'''








# query/vector_selector.py

import numpy as np

def combine_vectors(vectors, weights):
    """
    vectors: list of vectors or None
    weights: list of floats
    """
    combined = None
    total_weight = 0

    for vec, w in zip(vectors, weights):
        if vec is not None:
            if combined is None:
                combined = w * np.array(vec)
            else:
                combined += w * np.array(vec)
            total_weight += w

    if combined is None:
        return None

    return (combined / total_weight).tolist()

def select_search_vector(
    intent,
    query_vector,
    user_profile,
    session_vector
):
    """
    Priority:
    - Query intent (always)
    - Session intent (if exists)
    - User preference (if strong)
    """

    v_user = user_profile.get("preference_vector") if user_profile else None
    num_likes = user_profile.get("num_likes", 0) if user_profile else 0

    # Weights (can justify easily)
    w_query = 0.5
    w_session = 0.3
    w_user = 0.2 if num_likes >= 3 else 0.0

    final_vector = combine_vectors(
        [query_vector, session_vector, v_user],
        [w_query, w_session, w_user]
    )

    mode = "query_only"
    if session_vector and v_user:
        mode = "query+session+user"
    elif session_vector:
        mode = "query+session"
    elif v_user:
        mode = "query+user"

    return final_vector or query_vector, mode
