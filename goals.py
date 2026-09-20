def create_goal(goals, name, target):
    goals[name] = {
        "target": target,
        "saved": 0
    }


def add_to_goal(goals, name, amount):
    if name not in goals:
        return False

    goals[name]["saved"] += amount

    return True


def get_goal_progress(goals):

    progress = {}

    for name, goal in goals.items():

        target = goal["target"]
        saved = goal["saved"]

        remaining = max(target - saved, 0)

        percentage = (
            (saved / target) * 100
            if target > 0
            else 0
        )

        progress[name] = {
            "target": target,
            "saved": saved,
            "remaining": remaining,
            "percentage": percentage
        }

    return progress