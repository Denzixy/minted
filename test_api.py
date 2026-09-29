import os

import pytest
from fastapi.testclient import TestClient

import storage
from storage import initialize_database

from server import app


TEST_DATABASE = "test_minted.db"


@pytest.fixture(autouse=True)
def test_database():
    original_database = storage.DATABASE

    storage.DATABASE = TEST_DATABASE

    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)

    initialize_database()

    yield

    storage.DATABASE = original_database

    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)


@pytest.fixture
def client():
    return TestClient(app)


def test_get_transactions(client):
    response = client.get("/transactions")

    assert response.status_code == 200
    assert response.json() == []


def test_create_transaction(client):
    response = client.post(
        "/transactions",
        json={
            "amount": 50,
            "transaction_type": "expense",
            "category": "Food",
            "description": "Lunch"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["message"] == "Transaction created."


def test_create_and_get_transaction(client):
    create_response = client.post(
        "/transactions",
        json={
            "amount": 100,
            "transaction_type": "income",
            "category": "Allowance",
            "description": "Monthly allowance"
        }
    )

    assert create_response.status_code == 200

    transaction_id = create_response.json()["id"]

    response = client.get(
        f"/transactions/{transaction_id}"
    )

    assert response.status_code == 200

    transaction = response.json()

    assert transaction["amount"] == 100
    assert transaction["type"] == "income"
    assert transaction["category"] == "Allowance"


def test_update_transaction(client):
    create_response = client.post(
        "/transactions",
        json={
            "amount": 50,
            "transaction_type": "expense",
            "category": "Food",
            "description": "Lunch"
        }
    )

    transaction_id = create_response.json()["id"]

    response = client.put(
        f"/transactions/{transaction_id}",
        json={
            "amount": 75,
            "transaction_type": "expense",
            "category": "Shopping",
            "description": "New shirt"
        }
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/transactions/{transaction_id}"
    )

    transaction = get_response.json()

    assert transaction["amount"] == 75
    assert transaction["category"] == "Shopping"
    assert transaction["description"] == "New shirt"


def test_delete_transaction(client):
    create_response = client.post(
        "/transactions",
        json={
            "amount": 50,
            "transaction_type": "expense",
            "category": "Food",
            "description": "Lunch"
        }
    )

    transaction_id = create_response.json()["id"]

    response = client.delete(
        f"/transactions/{transaction_id}"
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/transactions/{transaction_id}"
    )

    assert get_response.status_code == 404


def test_invalid_transaction_type(client):
    response = client.post(
        "/transactions",
        json={
            "amount": 10,
            "transaction_type": "banana",
            "category": "Testing",
            "description": "Invalid transaction"
        }
    )

    assert response.status_code == 400


def test_get_dashboard(client):
    response = client.get(
        "/dashboard?year=2026&month=9"
    )

    assert response.status_code == 200

    data = response.json()

    assert "balance" in data
    assert "income" in data
    assert "expenses" in data
    assert "savings" in data
    assert "savings_rate" in data
    assert "spending" in data


def test_get_budgets(client):
    response = client.get(
        "/budgets?year=2026&month=9"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_create_budget(client):
    response = client.post(
        "/budgets",
        json={
            "category": "Food",
            "amount": 300,
            "year": 2026,
            "month": 9
        }
    )

    assert response.status_code == 200


def test_get_goals(client):
    response = client.get("/goals")

    assert response.status_code == 200
    assert response.json() == []


def test_create_goal(client):
    response = client.post(
        "/goals",
        json={
            "name": "New Laptop",
            "target": 5000,
            "saved": 500,
            "deadline": "2027-01-01"
        }
    )

    assert response.status_code == 200