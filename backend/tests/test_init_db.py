import pytest
from app.dao.database import init_db
import sqlite3

@pytest.mark.asyncio
async def test_init_db():
    # Call the init_db function to initialize the database
    try:
        await init_db()  
    except sqlite3.OperationalError as e:
        pytest.fail(f"OperationalError during test: {e}")

