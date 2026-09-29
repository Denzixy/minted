from storage import load_goals


def get_goal_data():

    rows = load_goals()

    goals = []

    for row in rows:

        name = row["name"]

        target = float(
            row["target"]
        )

        saved = float(
            row["saved"]
        )

        deadline = row["deadline"]

        remaining = max(
            target - saved,
            0
        )

        percentage = (
            (saved / target) * 100
            if target > 0
            else 0
        )

        goals.append({
            "name": name,
            "target": target,
            "saved": saved,
            "remaining": remaining,
            "percentage": min(
                percentage,
                100
            ),
            "deadline": deadline
        })

    return goals