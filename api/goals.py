from fastapi import APIRouter

from pydantic import (
    BaseModel,
    Field
)

from storage import save_goal

from services.goals import (
    get_goal_data
)


router = APIRouter(
    prefix="/goals",
    tags=["goals"]
)


class GoalCreate(BaseModel):

    name: str

    target: float = Field(
        gt=0
    )

    saved: float = Field(
        ge=0
    )

    deadline: str | None = None


@router.get("")
def get_goals():

    return get_goal_data()


@router.post("")
def create_goal(
    goal: GoalCreate
):

    save_goal(
        goal.name,
        goal.target,
        goal.saved,
        goal.deadline
    )

    return {
        "message": "Goal saved successfully."
    }