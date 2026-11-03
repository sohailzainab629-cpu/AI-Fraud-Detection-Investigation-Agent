
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import numpy as np
import joblib
import os

from backend.schemas import (
    TransactionRequest,
    ReviewDecisionRequest
)

from backend.agent import run_fraud_investigation

from backend.review import (
    create_review,
    get_review,
    get_all_reviews,
    make_decision
)


# =====================================
# PROJECT PATHS
# =====================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "fraud_model.pkl")


# =====================================
# INITIALIZE FASTAPI
# =====================================

app = FastAPI(
    title="Enterprise AI Fraud Detection & Investigation Agent",
    description="ML + FastAPI + LangGraph + Groq + Human Review",
    version="3.0.0"
)


# =====================================
# CORS CONFIGURATION
# =====================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5175",
"http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =====================================
# LOAD ML MODEL
# =====================================

try:
    model_bundle = joblib.load(MODEL_PATH)

    model = model_bundle["model"]
    feature_columns = model_bundle["feature_columns"]

    print("Fraud Detection Model Loaded Successfully!")

except Exception as e:
    raise RuntimeError(f"Model loading failed: {e}")


# =====================================
# REQUIRED FEATURES
# =====================================

REQUIRED_FEATURES = (
    ["Time"]
    + [f"V{i}" for i in range(1, 29)]
    + ["Amount"]
)


# =====================================
# PREPARE TRANSACTION
# =====================================

def prepare_transaction(transaction):

    missing_features = [
        feature
        for feature in REQUIRED_FEATURES
        if feature not in transaction
    ]

    if missing_features:
        raise ValueError(
            f"Missing features: {missing_features}"
        )

    values = [
        transaction[col]
        for col in REQUIRED_FEATURES
    ]

    if not np.isfinite(values).all():
        raise ValueError(
            "Feature values must be finite numbers."
        )

    if transaction["Time"] < 0 or transaction["Amount"] < 0:
        raise ValueError(
            "Time and Amount cannot be negative."
        )

    df = pd.DataFrame(
        [transaction],
        columns=REQUIRED_FEATURES
    )

    # Feature Engineering
    df["Hour"] = (df["Time"] / 3600) % 24
    df["Amount_log"] = np.log1p(df["Amount"])

    return df[feature_columns]


# =====================================
# HOME ENDPOINT
# =====================================

@app.get("/")
def home():

    return {
        "message": "Enterprise AI Fraud Detection API is running!",
        "status": "success"
    }


# =====================================
# HEALTH CHECK
# =====================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


# =====================================
# ML PREDICTION ENDPOINT
# =====================================

@app.post("/predict")
def predict_fraud(request: TransactionRequest):

    try:
        df = prepare_transaction(request.transaction)

        prediction = int(model.predict(df)[0])

        probability = float(
            model.predict_proba(df)[0][1]
        )

        return {
            "prediction": prediction,
            "result": (
                "Fraudulent" if prediction == 1 else "Legitimate"
            ),
            "fraud_probability": round(probability, 4),
            "message": "Transaction prediction completed successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# AI FRAUD INVESTIGATION ENDPOINT
# =====================================

@app.post("/investigate")
def investigate_fraud(request: TransactionRequest):

    try:
        df = prepare_transaction(request.transaction)

        prediction = int(model.predict(df)[0])

        probability = float(
            model.predict_proba(df)[0][1]
        )

        # Run LangGraph AI Agent
        investigation = run_fraud_investigation(
            prediction=prediction,
            fraud_probability=probability,
            amount=float(request.transaction["Amount"]),
            transaction_time=float(request.transaction["Time"])
        )

        # Create Human Review for High Risk
        review = None

        if investigation["risk_level"] == "High":

            review = create_review(
                prediction=prediction,
                fraud_probability=probability,
                amount=float(request.transaction["Amount"]),
                risk_level=investigation["risk_level"]
            )

        return {
            "prediction": prediction,
            "result": (
                "Fraudulent" if prediction == 1 else "Legitimate"
            ),
            "fraud_probability": round(probability, 4),
            "risk_level": investigation["risk_level"],
            "recommendation": investigation["recommendation"],
            "investigation_report": investigation[
                "investigation_report"
            ],
            "human_review": review
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Investigation failed: {str(e)}"
        )


# =====================================
# LIST ALL HUMAN REVIEWS
# =====================================

@app.get("/reviews")
def list_reviews():

    reviews = get_all_reviews()

    return {
        "total_reviews": len(reviews),
        "reviews": reviews
    }


# =====================================
# GET SINGLE REVIEW
# =====================================

@app.get("/reviews/{review_id}")
def review_details(review_id: str):

    review = get_review(review_id)

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    return review


# =====================================
# SUBMIT HUMAN REVIEW DECISION
# =====================================

@app.post("/reviews/{review_id}/decision")
def submit_review_decision(
    review_id: str,
    request: ReviewDecisionRequest
):

    try:
        review = make_decision(
            review_id,
            request.decision
        )

        if review is None:
            raise HTTPException(
                status_code=404,
                detail="Review not found"
            )

        return {
            "message": "Human review decision saved successfully",
            "review": review
        }

    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )
