from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    """Define an income or outcome financial transaction"""
    date: str
    category: str
    description: str
    amount: float
    updated_at: str

