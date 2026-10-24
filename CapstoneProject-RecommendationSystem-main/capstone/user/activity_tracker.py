# user/activity_tracker.py

import datetime
from db import db
from config import USER_ACTIVITY_COLLECTION

class ActivityTracker:
    def __init__(self):
        self.col = db[USER_ACTIVITY_COLLECTION]

    def log_event(self, user_id, item_id, item_type, event):
        self.col.insert_one({
            "user_id": user_id,
            "item_id": item_id,
            "item_type": item_type,  # "book" or "service"
            "event": event,          # view | click | like | dislike
            "timestamp": datetime.datetime.utcnow()
        })

    def get_recent_activity(self, user_id, limit=20):
        return list(
            self.col.find({"user_id": user_id})
            .sort("timestamp", -1)
            .limit(limit)
        )
