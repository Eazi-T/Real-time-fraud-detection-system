from pydantic import BaseModel
from typing import List

class Transaction(BaseModel):
    features: List[float]  # 30 values expected: ['Time', 'V1'...'V28', 'Amount']