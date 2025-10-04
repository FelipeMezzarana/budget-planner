# Third party
from fastapi import FastAPI, status

# Local
from . import __description__, __title__, __version__
from .clients.sqlite_client import SQLiteClient
from .data_models.transaction import Transaction
from .utils.constants import TRANSACTION_TABLE

app = FastAPI(
    version=__version__,
    title=__title__,
    description=__description__,
)

@app.post("/transaction/", status_code=status.HTTP_200_OK)
def insert_transaction(transaction: Transaction) -> dict:
    """Insert Transaction"""

    # Configure
    client = SQLiteClient()
    fields = list(Transaction.model_fields.keys())
    client.insert_data_model(transaction, fields, TRANSACTION_TABLE)

    return {"message": "Transaction created successfully"}

