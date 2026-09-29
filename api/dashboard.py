from datetime import datetime

from fastapi import (
    APIRouter,
    HTTPException
)

from services.dashboard import (
    get_dashboard_data
)


router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"]
)


@router.get("")
def dashboard(
    year: int | None = None,
    month: int | None = None
):

    now = datetime.now()

    if year is None:
        year = now.year

    if month is None:
        month = now.month

    if month < 1 or month > 12:

        raise HTTPException(
            status_code=400,
            detail="Month must be between 1 and 12."
        )

    return get_dashboard_data(
        year,
        month
    )