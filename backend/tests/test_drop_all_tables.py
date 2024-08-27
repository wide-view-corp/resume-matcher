import pytest
from app.dao.database import drop_all_tables

@pytest.mark.asyncio
async def test_drop_all_tables():
    await drop_all_tables()