import os
os.environ["ENV"] = "test"

import pytest
from db.seed.seed import drop_and_seed_tables

@pytest.fixture(autouse=True)
def seed_test_db():
    drop_and_seed_tables()