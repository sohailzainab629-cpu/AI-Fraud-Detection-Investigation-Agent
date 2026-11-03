
import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END


# Load environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


# Initialize Groq LLM
api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing in .env file")

llm = ChatGroq(
    model=model_name,
    api_key=api_key,
    temperature=0.2
)


# LangGraph State
class FraudState(TypedDict, total=False):
    prediction: int
    fraud_probability: float
    amount: float
    transaction_time: float
    risk_level: str
    recommendation: str
    investigation_report: str


# Node 1: Risk Assessment
def assess_risk(state: FraudState):

    probability = state["fraud_probability"]

    if probability >= 0.80:
        risk = "High"
        recommendation = "Block Transaction"

    elif probability >= 0.40:
        risk = "Medium"
        recommendation = "Hold for Review"

    else:
        risk = "Low"
        recommendation = "Approve Transaction"

    return {
        "risk_level": risk,
        "recommendation": recommendation
    }


# Node 2: AI Investigation
def investigate_transaction(state: FraudState):

    prompt = f"""
    You are an Enterprise Credit Card Fraud Investigation Agent.

    Analyze the following transaction information:

    ML Prediction: {state['prediction']}
    Fraud Probability: {state['fraud_probability']}
    Transaction Amount: {state['amount']}
    Transaction Time: {state['transaction_time']}
    Risk Level: {state['risk_level']}
    Recommended Action: {state['recommendation']}

    Write a professional investigation report containing:

    1. Transaction Summary
    2. ML Model Findings
    3. Risk Assessment
    4. Recommended Action
    5. Human Review Requirement

    Important:
    - Do not invent transaction details.
    - V1 to V28 are anonymized PCA features.
    - Do not claim to know their real-world meaning.
    - Fraud probability is a model estimate, not proof of fraud.
    - If risk is High, clearly state that human approval is required.
    """

    response = llm.invoke([
        SystemMessage(
            content="You are a professional financial fraud investigator."
        ),
        HumanMessage(content=prompt)
    ])

    return {
        "investigation_report": response.content
    }


# Build LangGraph workflow
workflow = StateGraph(FraudState)

workflow.add_node("assess_risk", assess_risk)
workflow.add_node("investigate", investigate_transaction)

workflow.add_edge(START, "assess_risk")
workflow.add_edge("assess_risk", "investigate")
workflow.add_edge("investigate", END)

fraud_agent = workflow.compile()


# Public function
def run_fraud_investigation(
    prediction: int,
    fraud_probability: float,
    amount: float,
    transaction_time: float
):

    initial_state = {
        "prediction": prediction,
        "fraud_probability": fraud_probability,
        "amount": amount,
        "transaction_time": transaction_time
    }

    result = fraud_agent.invoke(initial_state)

    return result
