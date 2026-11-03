
from pydantic import BaseModel, Field
from typing import Dict, Literal


class TransactionRequest(BaseModel):
    transaction: Dict[str, float] = Field(
        ...,
        description="Credit card transaction features"
    )


class ReviewDecisionRequest(BaseModel):
    decision: Literal["Approve", "Reject"] = Field(
        ...,
        description="Human review decision"
    )
