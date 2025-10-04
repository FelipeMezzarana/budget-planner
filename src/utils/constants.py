
import logging

# App
LOGGING_LEVEL = logging.DEBUG

# Database
DB_PATH = "database/app_backend.db"
DB_SCHEMA = "OPERATIONAL"
DB_TABLES = [
    {
        "name": "FINANCIAL_TRANSACTION",
        "schema": "OPERATIONAL",
        "fields_mapping": {
            "date": "DATE",
            "category": "VARCHAR(255)",
            "description": "VARCHAR(255)",
            "amount": "FLOAT",
            "updated_at": "DATETIME"
        }    
    }
]
TRANSACTION_TABLE = "FINANCIAL_TRANSACTION"