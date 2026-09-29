from datetime import datetime


def get_monthly_data(transactions, year, month):
    income = 0
    expenses = 0
    categories = {}

    for transaction in transactions:
        date = datetime.strptime(
            transaction.date,
            "%Y-%m-%d %H:%M"
        )

        if date.year != year or date.month != month:
            continue

        if transaction.transaction_type == "income":
            income += transaction.amount

        elif transaction.transaction_type == "expense":
            expenses += transaction.amount

            category = transaction.category

            if category not in categories:
                categories[category] = 0

            categories[category] += transaction.amount

    return income, expenses, categories


def generate_insights(transactions, year, month):
    insights = []

    income, expenses, categories = get_monthly_data(
        transactions,
        year,
        month
    )

    if income == 0 and expenses == 0:
        return [
            "Not enough data to generate insights yet."
        ]

    # -------------------------
    # SAVINGS
    # -------------------------

    savings = income - expenses

    if income > 0:

        savings_rate = (savings / income) * 100

        if savings_rate >= 30:
            insights.append(
                f"You're saving {savings_rate:.1f}% "
                "of your income this month."
            )

        elif savings_rate >= 10:
            insights.append(
                f"Your savings rate is "
                f"{savings_rate:.1f}% this month."
            )

        elif savings_rate >= 0:
            insights.append(
                "You're spending most of your income "
                "this month."
            )

        else:
            insights.append(
                "You're spending more than your income "
                "this month."
            )

    # -------------------------
    # TOP CATEGORY
    # -------------------------

    if categories:

        top_category = max(
            categories,
            key=categories.get
        )

        top_amount = categories[top_category]

        insights.append(
            f"{top_category} is your largest spending "
            f"category at RM {top_amount:.2f}."
        )

    # -------------------------
    # CATEGORY SHARE
    # -------------------------

    if expenses > 0:

        for category, amount in categories.items():

            percentage = (
                amount / expenses
            ) * 100

            if percentage >= 50:

                insights.append(
                    f"{category} makes up "
                    f"{percentage:.1f}% of your spending."
                )

    return insights

def compare_with_previous_month(
    transactions,
    year,
    month
):
    if month == 1:
        previous_year = year - 1
        previous_month = 12
    else:
        previous_year = year
        previous_month = month - 1

    current_income, current_expenses, _ = (
        get_monthly_data(
            transactions,
            year,
            month
        )
    )

    previous_income, previous_expenses, _ = (
        get_monthly_data(
            transactions,
            previous_year,
            previous_month
        )
    )

    insights = []

    if previous_expenses > 0:

        change = (
            (current_expenses - previous_expenses)
            / previous_expenses
        ) * 100

        if change > 0:
            insights.append(
                f"Your spending is up "
                f"{change:.1f}% compared with "
                "last month."
            )

        elif change < 0:
            insights.append(
                f"Your spending is down "
                f"{abs(change):.1f}% compared with "
                "last month."
            )

        else:
            insights.append(
                "Your spending is unchanged "
                "from last month."
            )

    if previous_income > 0:

        income_change = (
            (current_income - previous_income)
            / previous_income
        ) * 100

        if income_change != 0:

            direction = (
                "up"
                if income_change > 0
                else "down"
            )

            insights.append(
                f"Your income is {direction} "
                f"{abs(income_change):.1f}% "
                "compared with last month."
            )

    return insights