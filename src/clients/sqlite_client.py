# Standard library
import os
import re
import sqlite3
from pydantic import BaseModel

# Local
from ..exceptions import DirectoryCreationError
from ..utils.get_logger import get_logger
from ..utils.constants import DB_PATH, DB_TABLES
from ..utils.decorators import singleton

@singleton
class SQLiteClient:
    """SQLite Client."""

    def __init__(self):
        """Setup settings."""

        self.logger = get_logger(__name__)
        self.logger.debug(f"Initializing SQLiteClient...")
        self.DB_PATH = DB_PATH
        # Create db file if not exist
        self.check_db(self.DB_PATH)
        self.logger.debug(f"{self.DB_PATH=}")
        self.connect()
        for table_config in DB_TABLES:
            self.create_table(table_config)
        self.logger.debug(f"Initializing completed.")

    def connect(self):
        """Connect to db."""
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cur = self.conn.cursor()
        self.logger.info("connected")

    def execute(self, query: str) -> list[tuple]:
        """Execute query."""

        resp = self.cur.execute(query)
        self.conn.commit()

        return resp.fetchall()

    def insert_data_model(self, data_model: BaseModel, fields:list[str], table: str):
        """Insert model into table"""

        fields_str = ", ".join(fields)   
        placeholders = ", ".join(["?"] * len(fields))
        sql = f"INSERT INTO {table} ({fields_str}) VALUES ({placeholders})"
        values = list(data_model.model_dump().values())
        self.logger.debug(f"Executing sql query: {sql}")
        self.logger.debug(f"{values=}")

        self.execute_many(sql, [values])

    def execute_many(self, query: str, mapped_values: list[tuple]):
        """Execute parameterized query."""
        self.cur.executemany(query, mapped_values)
        self.conn.commit()

    def create_table(self, table_config: list[dict]):
        """Create table if not exists"""

        # Build SQL statement
        table_name = table_config["name"]
        table_fields = table_config["fields_mapping"]
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} \n ("
        for field, data_type in table_fields.items():
            create_table_sql += f"{field} {data_type}\n, "
        create_table_sql = create_table_sql.strip(", ")
        create_table_sql += " )"
        self.logger.debug(f"Creating table if not exist: {table_name}")

        # Create Table
        self.execute(create_table_sql)


    def check_db(self, db_path):
        """Check if SQLite file exist, creates a new one if not."""

        if not os.path.exists(db_path):
            self.logger.info
            (f"Database file {db_path} not fount. A new file will be created")
            # Check directory
            if re.search("/", db_path):
                try:
                    directory = re.findall(r"([^\/]*)/[^\/]*.db", db_path)[0]
                    if not os.path.exists(directory):
                        os.mkdir(directory)
                        self.logger.info(f"DB directory not found. Created {directory}")
                    else:
                        self.logger.info(f"DB directory found. {directory=}")
                except Exception as err:  # pragma: no cover
                    raise DirectoryCreationError(directory, err)
