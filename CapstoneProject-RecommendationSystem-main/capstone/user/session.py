# user/session.py

import numpy as np
from db import db
from bson import ObjectId
from config import USER_ACTIVITY_COLLECTION, BOOKS_COLLECTION, SERVICES_COLLECTION

class SessionProfiler:
    def __init__(self):
        self.activity = db[USER_ACTIVITY_COLLECTION]
        self.books = db[BOOKS_COLLECTION]
        self.services = db[SERVICES_COLLECTION]

    def _fetch_embedding(self, item_id, item_type):
        col = self.books if item_type == "book" else self.services
        #doc = col.find_one({"_id": item_id}, {"embedding": 1})
        doc = col.find_one({"_id": ObjectId(item_id)}, {"embedding": 1})
        return doc["embedding"] if doc else None

    def build_session_vector(self, user_id, limit=5):
        """
        Uses most recent interactions in the session
        """
        '''events = list(
            self.activity.find(
                {"user_id": user_id, "event": {"$in": ["view", "click", "like"]}}
            )
            .sort("timestamp", -1)
            .limit(limit)
        )'''
        events = list(
            self.activity.find(
                {"user_id": user_id, "event": {"$in": ["view", "click", "like"]}}
            ).sort("timestamp", -1).limit(limit)
        )


        vectors = []
        for e in events:
            vec = self._fetch_embedding(e["item_id"], e["item_type"])
            if vec:
                vectors.append(vec)

        if not vectors:
            return None

        return np.mean(np.array(vectors), axis=0).tolist()
