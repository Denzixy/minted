from fastapi import APIRouter, HTTPException

from pydantic import BaseModel, Field

from storage import (
    save_goal,
    delete_goal
)

from services.goals import get_goal_data


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

@router.put("/{name}")
def update_goal(name: str, goal: GoalCreate):
    save_goal(
        name,
        goal.target,
        goal.saved,
        goal.deadline
    )

    return {"message": "Goal updated successfully."}


@router.delete("/{name}")
def remove_goal(name: str):
    deleted = delete_goal(name)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Goal not found."
        )

    return {
        "message": "Goal deleted successfully."
    }