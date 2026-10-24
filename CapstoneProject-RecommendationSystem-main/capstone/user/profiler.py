# user/profiler.py

import datetime
import numpy as np
from db import db
from config import USERS_COLLECTION, BOOKS_COLLECTION, SERVICES_COLLECTION

class UserProfiler:
    def __init__(self):
        self.users = db[USERS_COLLECTION]
        self.books = db[BOOKS_COLLECTION]
        self.services = db[SERVICES_COLLECTION]

    def get_user(self, user_id):
        return self.users.find_one({"user_id": user_id})

    def create_user_if_not_exists(self, user_id):
        if not self.get_user(user_id):
            self.users.insert_one({
                "user_id": user_id,
                "is_guest": user_id.startswith("guest"),
                "liked_items": [],
                "preference_vector": None,
                "num_likes": 0,
                "last_updated": None
            })

    def _fetch_item_embedding(self, item_id, item_type):
        col = self.books if item_type == "book" else self.services
        doc = col.find_one({"_id": item_id}, {"embedding": 1})
        return doc["embedding"] if doc else None

    def update_on_like(self, user_id, item_id, item_type):
        self.create_user_if_not_exists(user_id)

        embedding = self._fetch_item_embedding(item_id, item_type)
        if embedding is None:
            return

        user = self.get_user(user_id)

        liked = user["liked_items"]
        liked.append({
            "item_id": item_id,
            "item_type": item_type
        })

        # Build V_user = mean of liked item vectors
        vectors = []
        for li in liked:
            vec = self._fetch_item_embedding(li["item_id"], li["item_type"])
            if vec:
                vectors.append(vec)

        if not vectors:
            return

        v_user = np.mean(np.array(vectors), axis=0).tolist()

        self.users.update_one(
            {"user_id": user_id},
            {"$set": {
                "liked_items": liked,
                "preference_vector": v_user,
                "num_likes": len(liked),
                "last_updated": datetime.datetime.utcnow()
            }}
        )

    def has_strong_profile(self, user_id, min_likes=3):
        user = self.get_user(user_id)
        return user and user["num_likes"] >= min_likes
