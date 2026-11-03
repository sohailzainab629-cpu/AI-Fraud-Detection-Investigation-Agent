
import json
import os
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW_FILE = os.path.join(BASE_DIR, "reports", "pending_reviews.json")


def load_reviews():
    os.makedirs(os.path.dirname(REVIEW_FILE), exist_ok=True)

    if not os.path.exists(REVIEW_FILE):
        return {}

    try:
        with open(REVIEW_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        raise RuntimeError("Review data file contains invalid JSON.")


def save_reviews(reviews):
    os.makedirs(os.path.dirname(REVIEW_FILE), exist_ok=True)

    with open(REVIEW_FILE, "w", encoding="utf-8") as file:
        json.dump(reviews, file, indent=4)


def create_review(prediction, fraud_probability, amount, risk_level):
    reviews = load_reviews()

    review_id = f"REV-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"

    review = {
        "review_id": review_id,
        "prediction": prediction,
        "fraud_probability": round(fraud_probability, 4),
        "amount": amount,
        "risk_level": risk_level,
        "status": "Pending",
        "decision": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "reviewed_at": None
    }

    reviews[review_id] = review
    save_reviews(reviews)

    return review


def get_review(review_id):
    reviews = load_reviews()
    return reviews.get(review_id)


def get_all_reviews():
    return list(load_reviews().values())


def make_decision(review_id, decision):
    reviews = load_reviews()

    if review_id not in reviews:
        return None

    if reviews[review_id]["status"] != "Pending":
        raise ValueError("This review has already been decided.")

    reviews[review_id]["status"] = "Reviewed"
    reviews[review_id]["decision"] = decision
    reviews[review_id]["reviewed_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    save_reviews(reviews)

    return reviews[review_id]
