from fastapi import FastAPI

from fastapi.staticfiles import (
    StaticFiles
)

from storage import (
    initialize_database
)

from api.transactions import (
    router as transactions_router
)

from api.budgets import (
    router as budgets_router
)

from api.dashboard import (
    router as dashboard_router
)

from api.goals import (
    router as goals_router
)


app = FastAPI(
    title="Minted API",
    description="Personal finance API for Minted.",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    initialize_database()


app.include_router(
    transactions_router
)

app.include_router(
    budgets_router
)

app.include_router(
    dashboard_router
)

app.include_router(
    goals_router
)


app.mount(
    "/",
    StaticFiles(
        directory="frontend",
        html=True
    ),
    name="frontend"
)