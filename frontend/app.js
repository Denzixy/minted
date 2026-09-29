const API_URL = "";

let transactions = [];

let selectedDate = new Date();

let spendingChart = null;


async function loadTransactions() {

    try {

        const response = await fetch(
            `${API_URL}/transactions`
        );

        transactions = await response.json();

        displayTransactions();
        await loadDashboard();

    } catch (error) {

        console.error(error);

        document.getElementById(
            "transactions"
        ).innerHTML =
            "<p>Could not connect to Minted API.</p>";
    }
}


function displayTransactions() {

    const container =
        document.getElementById(
            "transactions"
        );


    if (transactions.length === 0) {

        container.innerHTML =
            "<p>No transactions yet.</p>";

        return;
    }


    const recent =
        [...transactions]
        .reverse()
        .slice(0, 8);


    container.innerHTML =
        recent.map(transaction => {

            const sign =
                transaction.type === "income"
                    ? "+"
                    : "-";


            const className =
                transaction.type === "income"
                    ? "income"
                    : "expense";


            return `
                <div class="transaction">

                    <div class="transaction-info">

                        <strong>
                            ${transaction.description}
                        </strong>

                        <span>
                            ${transaction.category}
                            ·
                            ${transaction.date}
                        </span>

                    </div>

                    <strong class="${className}">
                        ${sign}
                        RM ${Number(
                            transaction.amount
                        ).toFixed(2)}
                    </strong>

                </div>
            `;

        }).join("");
}


async function loadDashboard() {

    try {

        const year =
            selectedDate.getFullYear();

        const month =
            selectedDate.getMonth() + 1;

        const response = await fetch(
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

    } catch (error) {

        console.error(error);

    }
}

function changeMonth(direction) {

    selectedDate.setMonth(
        selectedDate.getMonth() + direction
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


function displaySpending(spending) {

    const container =
        document.getElementById("spending");

    const categories =
        Object.entries(spending)
        .sort((a, b) => b[1] - a[1]);

    if (categories.length === 0) {

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
        new Chart(canvas, {

            type: "doughnut",

            data: {

                labels: labels,

                datasets: [{
                    data: values
                }]

            },

            options: {

                responsive: true,

                plugins: {

                    legend: {
                        position: "bottom"
                    }

                }

            }

        });
}


function openTransactionModal() {

    document
        .getElementById(
            "transaction-modal"
        )
        .classList
        .remove("hidden");
}


function closeTransactionModal() {

    document
        .getElementById(
            "transaction-modal"
        )
        .classList
        .add("hidden");
}


document
    .getElementById("transaction-form")
    .addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const transaction = {

                amount: Number(
                    document
                        .getElementById("amount")
                        .value
                ),

                transaction_type:
                    document
                        .getElementById("type")
                        .value,

                category:
                    document
                        .getElementById("category")
                        .value,

                description:
                    document
                        .getElementById("description")
                        .value

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


            } catch (error) {

                console.error(error);

                alert(
                    "Could not add transaction."
                );

            }

        }
    );


loadTransactions();