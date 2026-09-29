const API_URL = "";


/* =========================================
   GLOBAL STATE
========================================= */

let transactions = [];

let selectedDate = new Date();

let budgetDate = new Date();

let spendingChart = null;


/* =========================================
   PAGE NAVIGATION
========================================= */

function showPage(
    pageId,
    button
) {

    document
        .querySelectorAll(".page")
        .forEach(page => {

            page.classList.add(
                "hidden"
            );

        });


    const page = document.getElementById(
        pageId
    );

    if (page) {

        page.classList.remove(
            "hidden"
        );

    }


    document
        .querySelectorAll(".nav-item")
        .forEach(item => {

            item.classList.remove(
                "active"
            );

        });


    if (button) {

        button.classList.add(
            "active"
        );

    }


    if (
        pageId ===
        "dashboard-page"
    ) {

        loadDashboard();

    }


    if (
        pageId ===
        "transactions-page"
    ) {

        loadAllTransactions();

    }


    if (
        pageId ===
        "budgets-page"
    ) {

        loadBudgets();

    }


    if (
        pageId ===
        "goals-page"
    ) {

        loadGoals();

    }
}


/* =========================================
   DASHBOARD
========================================= */

async function loadDashboard() {

    try {

        const year =
            selectedDate.getFullYear();

        const month =
            selectedDate.getMonth() + 1;


        const response =
            await fetch(
                `${API_URL}/dashboard?year=${year}&month=${month}`
            );


        if (!response.ok) {

            throw new Error(
                "Failed to load dashboard"
            );

        }


        const dashboard =
            await response.json();


        document.getElementById(
            "balance"
        ).textContent =
            `RM ${dashboard.balance.toFixed(2)}`;


        document.getElementById(
            "income"
        ).textContent =
            `RM ${dashboard.income.toFixed(2)}`;


        document.getElementById(
            "expenses"
        ).textContent =
            `RM ${dashboard.expenses.toFixed(2)}`;


        document.getElementById(
            "savings-rate"
        ).textContent =
            `${dashboard.savings_rate.toFixed(1)}%`;


        updateMonthLabel();

        displaySpending(
            dashboard.spending
        );


        await loadTransactions();

    } catch (error) {

        console.error(
            error
        );

    }
}


function changeMonth(
    direction
) {

    selectedDate.setMonth(
        selectedDate.getMonth()
        + direction
    );

    loadDashboard();
}


function updateMonthLabel() {

    const label =
        selectedDate.toLocaleDateString(
            "en-US",
            {
                month: "long",
                year: "numeric"
            }
        );


    document.getElementById(
        "current-month"
    ).textContent = label;
}


function displaySpending(
    spending
) {

    const container =
        document.getElementById(
            "spending"
        );


    const categories =
        Object.entries(
            spending
        ).sort(
            (a, b) => b[1] - a[1]
        );


    if (
        categories.length === 0
    ) {

        container.innerHTML =
            "<p>No spending this month.</p>";


        if (spendingChart) {

            spendingChart.destroy();

            spendingChart = null;

        }

        return;
    }


    container.innerHTML = `
        <div class="chart-container">
            <canvas id="spending-chart"></canvas>
        </div>
    `;


    const labels =
        categories.map(
            item => item[0]
        );


    const values =
        categories.map(
            item => item[1]
        );


    const canvas =
        document.getElementById(
            "spending-chart"
        );


    if (spendingChart) {

        spendingChart.destroy();

    }


    spendingChart =
        new Chart(
            canvas,
            {
                type: "doughnut",

                data: {

                    labels: labels,

                    datasets: [
                        {
                            data: values
                        }
                    ]

                },

                options: {

                    responsive: true,

                    plugins: {

                        legend: {
                            position:
                                "bottom"
                        }

                    }

                }

            }
        );
}


/* =========================================
   TRANSACTIONS
========================================= */

async function loadTransactions() {

    try {

        const response =
            await fetch(
                `${API_URL}/transactions`
            );


        if (!response.ok) {

            throw new Error(
                "Failed to load transactions"
            );

        }


        transactions =
            await response.json();


        displayTransactions();

    } catch (error) {

        console.error(
            error
        );


        document.getElementById(
            "transactions"
        ).innerHTML =
            "<p>Could not connect to Minted API.</p>";

    }
}


async function loadAllTransactions() {

    await loadTransactions();

    displayAllTransactions();

}


function displayAllTransactions() {
    const container = document.getElementById(
        "all-transactions"
    );

    if (!container) return;

    const search = (
        document.getElementById("transaction-search")?.value || ""
    ).trim().toLowerCase();

    const typeFilter =
        document.getElementById("transaction-type-filter")?.value
        || "all";

    const sortOrder =
        document.getElementById("transaction-sort")?.value
        || "newest";

    let filtered = transactions.filter(transaction => {
        const matchesSearch =
            transaction.description.toLowerCase().includes(search) ||
            transaction.category.toLowerCase().includes(search);

        const matchesType =
            typeFilter === "all" ||
            transaction.type === typeFilter;

        return matchesSearch && matchesType;
    });

    filtered.sort((a, b) => {
        if (sortOrder === "newest") {
            return b.id - a.id;
        }

        if (sortOrder === "oldest") {
            return a.id - b.id;
        }

        if (sortOrder === "highest") {
            return b.amount - a.amount;
        }

        if (sortOrder === "lowest") {
            return a.amount - b.amount;
        }

        return 0;
    });

    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="empty-budget">
                <h3>No matching transactions</h3>
                <p>
                    Try a different search or change your filters.
                </p>
            </div>
        `;
        return;
    }

    container.innerHTML = filtered.map(transaction => {
        const isIncome = transaction.type === "income";

        return `
            <div class="transaction">
                <div class="transaction-left">
                    <div class="transaction-icon">
                        ${isIncome ? "↑" : "↓"}
                    </div>

                    <div class="transaction-info">
                        <strong>
                            ${escapeHtml(transaction.description)}
                        </strong>

                        <span>
                            ${escapeHtml(transaction.category)}
                            ·
                            ${escapeHtml(transaction.date)}
                        </span>
                    </div>
                </div>

                <div class="transaction-actions">
                    <div class="transaction-amount ${
                        isIncome ? "income" : "expense"
                    }">
                        ${isIncome ? "+" : "-"}
                        RM ${Number(transaction.amount).toFixed(2)}
                    </div>

                    <button
                        class="action-button"
                        onclick="editTransaction(${transaction.id})"
                    >
                        Edit
                    </button>

                    <button
                        class="action-button delete-button"
                        onclick="deleteTransaction(${transaction.id})"
                    >
                        Delete
                    </button>
                </div>
            </div>
        `;
    }).join("");
}

let editingTransactionId = null;

function editTransaction(transactionId) {
    const transaction = transactions.find(
        item => item.id === transactionId
    );

    if (!transaction) {
        alert("Transaction not found.");
        return;
    }

    editingTransactionId = transactionId;

    document.getElementById(
        "edit-transaction-type"
    ).value = transaction.type;

    document.getElementById(
        "edit-transaction-amount"
    ).value = transaction.amount;

    document.getElementById(
        "edit-transaction-category"
    ).value = transaction.category;

    document.getElementById(
        "edit-transaction-description"
    ).value = transaction.description;

    document.getElementById(
        "edit-transaction-modal"
    ).classList.remove("hidden");
}

function closeEditTransactionModal() {
    document.getElementById(
        "edit-transaction-modal"
    ).classList.add("hidden");

    editingTransactionId = null;
}

document
    .getElementById("edit-transaction-form")
    .addEventListener("submit", async function(event) {
        event.preventDefault();

        if (editingTransactionId === null) {
            return;
        }

        const transaction = {
            amount: Number(
                document.getElementById(
                    "edit-transaction-amount"
                ).value
            ),
            transaction_type:
                document.getElementById(
                    "edit-transaction-type"
                ).value,
            category:
                document.getElementById(
                    "edit-transaction-category"
                ).value.trim(),
            description:
                document.getElementById(
                    "edit-transaction-description"
                ).value.trim()
        };

        if (
            !transaction.category ||
            !transaction.description ||
            transaction.amount <= 0
        ) {
            alert("Please enter valid transaction details.");
            return;
        }

        try {
            const response = await fetch(
                `${API_URL}/transactions/${editingTransactionId}`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(transaction)
                }
            );

            if (!response.ok) {
                throw new Error("Failed to update transaction");
            }

            closeEditTransactionModal();

            await loadTransactions();
            await loadDashboard();

            if (
                !document
                    .getElementById("transactions-page")
                    .classList.contains("hidden")
            ) {
                displayAllTransactions();
            }

        } catch (error) {
            console.error(error);
            alert("Could not update transaction.");
        }
    });


async function deleteTransaction(
    transactionId
) {
    const transaction = transactions.find(
        item => item.id === transactionId
    );

    if (!transaction) {
        alert("Transaction not found.");
        return;
    }

    const confirmed = confirm(
        `Delete "${transaction.description}"?`
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/transactions/${transactionId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error(
                "Failed to delete transaction"
            );
        }

        await loadTransactions();
        await loadDashboard();

        if (
            !document
                .getElementById("transactions-page")
                .classList.contains("hidden")
        ) {
            displayAllTransactions();
        }

    } catch (error) {
        console.error(error);

        alert(
            "Could not delete transaction."
        );
    }
}

function openTransactionModal() {

    document
        .getElementById(
            "transaction-modal"
        )
        .classList.remove(
            "hidden"
        );
}


function closeTransactionModal() {

    document
        .getElementById(
            "transaction-modal"
        )
        .classList.add(
            "hidden"
        );
}


document
    .getElementById(
        "transaction-form"
    )
    .addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const transaction = {

                amount: Number(
                    document.getElementById(
                        "transaction-amount"
                    ).value
                ),

                transaction_type:
                    document.getElementById(
                        "transaction-type"
                    ).value,

                category:
                    document.getElementById(
                        "transaction-category"
                    ).value,

                description:
                    document.getElementById(
                        "transaction-description"
                    ).value

            };


            try {

                const response =
                    await fetch(
                        `${API_URL}/transactions`,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    transaction
                                )
                        }
                    );


                if (!response.ok) {

                    throw new Error(
                        "Failed to create transaction"
                    );

                }


                document
                    .getElementById(
                        "transaction-form"
                    )
                    .reset();


                closeTransactionModal();


                await loadTransactions();

                await loadDashboard();

            } catch (error) {

                console.error(
                    error
                );

                alert(
                    "Could not save transaction."
                );

            }

        }
    );


/* =========================================
   BUDGETS
========================================= */

async function loadBudgets() {

    const year =
        budgetDate.getFullYear();

    const month =
        budgetDate.getMonth() + 1;


    try {

        const response =
            await fetch(
                `${API_URL}/budgets?year=${year}&month=${month}`
            );


        if (!response.ok) {

            throw new Error(
                "Failed to load budgets"
            );

        }


        const budgets =
            await response.json();


        displayBudgets(
            budgets
        );


        updateBudgetMonth();

    } catch (error) {

        console.error(
            error
        );


        document.getElementById(
            "budget-list"
        ).innerHTML =
            "<p>Could not load budgets.</p>";

    }
}


function displayBudgets(budgets) {
    const container = document.getElementById("budget-list");

    if (budgets.length === 0) {
        container.innerHTML = `
            <div class="empty-budget">
                <h3>No budgets yet</h3>
                <p>Create a budget to start tracking your spending.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = budgets.map(budget => {
        const percentage = Math.min(budget.percentage, 100);

        const status = budget.over_budget
            ? "Over budget"
            : `RM ${budget.remaining.toFixed(2)} remaining`;

        return `
            <div class="budget-card">
                <div class="budget-header">
                    <div>
                        <h3>${escapeHtml(budget.category)}</h3>
                        <p>
                            RM ${budget.spent.toFixed(2)}
                            / RM ${budget.budget.toFixed(2)}
                        </p>
                    </div>
                    <strong>${budget.percentage.toFixed(0)}%</strong>
                </div>

                <div class="progress-track">
                    <div class="progress-bar ${budget.over_budget ? "over" : ""}"
                         style="width:${percentage}%"></div>
                </div>

                <div class="budget-footer">
                    <span>${status}</span>
                </div>

                <div class="management-actions">
                    <button class="action-button"
                        onclick="editBudget('${escapeHtml(budget.category)}', ${budget.budget})">
                        Edit
                    </button>
                    <button class="action-button delete-button"
                        onclick="removeBudget('${escapeHtml(budget.category)}')">
                        Delete
                    </button>
                </div>
            </div>
        `;
    }).join("");
}

async function editBudget(category, currentAmount) {
    const amount = prompt("New monthly budget (RM):", currentAmount);

    if (amount === null) return;

    const value = Number(amount);

    if (!Number.isFinite(value) || value <= 0) {
        alert("Enter a valid budget amount.");
        return;
    }

    const response = await fetch(
        `${API_URL}/budgets/${encodeURIComponent(category)}`,
        {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                category,
                amount: value,
                year: budgetDate.getFullYear(),
                month: budgetDate.getMonth() + 1
            })
        }
    );

    if (!response.ok) {
        alert("Could not update budget.");
        return;
    }

    await loadBudgets();
}

async function removeBudget(category) {
    if (!confirm(`Delete the ${category} budget?`)) return;

    const year = budgetDate.getFullYear();
    const month = budgetDate.getMonth() + 1;

    const response = await fetch(
        `${API_URL}/budgets/${encodeURIComponent(category)}?year=${year}&month=${month}`,
        {method: "DELETE"}
    );

    if (!response.ok) {
        alert("Could not delete budget.");
        return;
    }

    await loadBudgets();
}


function changeBudgetMonth(
    direction
) {

    budgetDate.setMonth(
        budgetDate.getMonth()
        + direction
    );

    loadBudgets();
}


function updateBudgetMonth() {

    const label =
        budgetDate.toLocaleDateString(
            "en-US",
            {
                month: "long",
                year: "numeric"
            }
        );


    document.getElementById(
        "budget-month"
    ).textContent = label;
}


function openBudgetModal() {

    document
        .getElementById(
            "budget-modal"
        )
        .classList.remove(
            "hidden"
        );
}


function closeBudgetModal() {

    document
        .getElementById(
            "budget-modal"
        )
        .classList.add(
            "hidden"
        );
}


document
    .getElementById(
        "budget-form"
    )
    .addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const budget = {

                category:
                    document.getElementById(
                        "budget-category"
                    ).value,

                amount: Number(
                    document.getElementById(
                        "budget-amount"
                    ).value
                ),

                year:
                    budgetDate.getFullYear(),

                month:
                    budgetDate.getMonth() + 1

            };


            try {

                const response =
                    await fetch(
                        `${API_URL}/budgets`,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    budget
                                )
                        }
                    );


                if (!response.ok) {

                    throw new Error(
                        "Failed to save budget"
                    );

                }


                document
                    .getElementById(
                        "budget-form"
                    )
                    .reset();


                closeBudgetModal();


                loadBudgets();

            } catch (error) {

                console.error(
                    error
                );

                alert(
                    "Could not save budget."
                );

            }

        }
    );


/* =========================================
   GOALS
========================================= */

async function loadGoals() {

    try {

        const response =
            await fetch(
                `${API_URL}/goals`
            );


        if (!response.ok) {

            throw new Error(
                "Failed to load goals"
            );

        }


        const goals =
            await response.json();


        displayGoals(
            goals
        );

    } catch (error) {

        console.error(
            error
        );


        document.getElementById(
            "goal-list"
        ).innerHTML =
            "<p>Could not load goals.</p>";

    }
}


function displayGoals(goals) {
    const container = document.getElementById("goal-list");

    if (goals.length === 0) {
        container.innerHTML = `
            <div class="empty-budget">
                <h3>No goals yet</h3>
                <p>Create a goal and start tracking your progress.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = goals.map(goal => `
        <div class="goal-card">
            <div class="goal-header">
                <div>
                    <h3>${escapeHtml(goal.name)}</h3>
                    <p>${goal.deadline ? `Target: ${escapeHtml(goal.deadline)}` : "No deadline"}</p>
                </div>
                <strong>${goal.percentage.toFixed(0)}%</strong>
            </div>

            <div class="goal-amount">
                RM ${goal.saved.toFixed(2)}
                <span>/ RM ${goal.target.toFixed(2)}</span>
            </div>

            <div class="progress-track">
                <div class="progress-bar" style="width:${goal.percentage}%"></div>
            </div>

            <div class="goal-footer">
                <span>RM ${goal.remaining.toFixed(2)} remaining</span>
            </div>

            <div class="management-actions">
                <button class="action-button"
                    onclick="editGoal('${escapeHtml(goal.name)}', ${goal.target}, ${goal.saved}, '${goal.deadline || ""}')">
                    Edit
                </button>
                <button class="action-button delete-button"
                    onclick="removeGoal('${escapeHtml(goal.name)}')">
                    Delete
                </button>
            </div>
        </div>
    `).join("");
}

async function editGoal(name, target, saved, deadline) {
    const newTarget = prompt("Target amount (RM):", target);
    if (newTarget === null) return;

    const newSaved = prompt("Amount saved (RM):", saved);
    if (newSaved === null) return;

    const newDeadline = prompt("Deadline (YYYY-MM-DD, optional):", deadline);
    if (newDeadline === null) return;

    const targetValue = Number(newTarget);
    const savedValue = Number(newSaved);

    if (
        !Number.isFinite(targetValue) || targetValue <= 0 ||
        !Number.isFinite(savedValue) || savedValue < 0
    ) {
        alert("Enter valid amounts.");
        return;
    }

    const response = await fetch(
        `${API_URL}/goals/${encodeURIComponent(name)}`,
        {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                name,
                target: targetValue,
                saved: savedValue,
                deadline: newDeadline || null
            })
        }
    );

    if (!response.ok) {
        alert("Could not update goal.");
        return;
    }

    await loadGoals();
}

async function removeGoal(name) {
    const confirmed = confirm(
        `Delete the "${name}" savings goal?`
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/goals/${encodeURIComponent(name)}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            const error = await response.json();
            console.error(error);

            alert(
                error.detail ||
                "Could not delete goal."
            );

            return;
        }

        await loadGoals();

    } catch (error) {
        console.error(error);
        alert("Could not connect to Minted API.");
    }
}


function openGoalModal() {

    document
        .getElementById(
            "goal-modal"
        )
        .classList.remove(
            "hidden"
        );
}


function closeGoalModal() {

    document
        .getElementById(
            "goal-modal"
        )
        .classList.add(
            "hidden"
        );
}


document
    .getElementById(
        "goal-form"
    )
    .addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const goal = {

                name:
                    document.getElementById(
                        "goal-name"
                    ).value,

                target: Number(
                    document.getElementById(
                        "goal-target"
                    ).value
                ),

                saved: Number(
                    document.getElementById(
                        "goal-saved"
                    ).value
                ),

                deadline:
                    document.getElementById(
                        "goal-deadline"
                    ).value
                    || null

            };


            try {

                const response =
                    await fetch(
                        `${API_URL}/goals`,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    goal
                                )
                        }
                    );


                if (!response.ok) {

                    throw new Error(
                        "Failed to create goal"
                    );

                }


                document
                    .getElementById(
                        "goal-form"
                    )
                    .reset();


                closeGoalModal();


                loadGoals();

            } catch (error) {

                console.error(
                    error
                );

                alert(
                    "Could not create goal."
                );

            }

        }
    );


/* =========================================
   SECURITY / HTML ESCAPING
========================================= */

function escapeHtml(
    value
) {

    return String(value)
        .replaceAll(
            "&",
            "&amp;"
        )
        .replaceAll(
            "<",
            "&lt;"
        )
        .replaceAll(
            ">",
            "&gt;"
        )
        .replaceAll(
            '"',
            "&quot;"
        )
        .replaceAll(
            "'",
            "&#039;"
        );
}


/* =========================================
   INITIAL LOAD
========================================= */

loadDashboard();

loadBudgets();

loadGoals();