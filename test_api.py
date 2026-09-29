from fastapi.testclient import TestClient

from server import app


client = TestClient(app)


def test_get_transactions():
    response = client.get("/transactions")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_dashboard():
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


def test_get_budgets():
    response = client.get(
        "/budgets?year=2026&month=9"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_goals():
    response = client.get("/goals")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_transaction():
    response = client.post(
        "/transactions",
        json={
            "amount": 10,
            "transaction_type": "expense",
            "category": "Testing",
            "description": "Automated test"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["message"] == "Transaction created."


def test_invalid_transaction_type():
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