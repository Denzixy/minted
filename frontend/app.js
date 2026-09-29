const API_URL = "http://127.0.0.1:8000";


let transactions = [];


async function loadTransactions() {

    try {

        const response = await fetch(
            `${API_URL}/transactions`
        );

        transactions = await response.json();

        displayTransactions();

        updateDashboard();

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


function updateDashboard() {

    let income = 0;
    let expenses = 0;


    transactions.forEach(transaction => {

        if (transaction.type === "income") {

            income += Number(
                transaction.amount
            );

        } else {

            expenses += Number(
                transaction.amount
            );

        }

    });


    const balance =
        income - expenses;


    const savingsRate =
        income > 0
            ? ((balance / income) * 100)
            : 0;


    document.getElementById(
        "balance"
    ).textContent =
        `RM ${balance.toFixed(2)}`;


    document.getElementById(
        "income"
    ).textContent =
        `RM ${income.toFixed(2)}`;


    document.getElementById(
        "expenses"
    ).textContent =
        `RM ${expenses.toFixed(2)}`;


    document.getElementById(
        "savings-rate"
    ).textContent =
        `${savingsRate.toFixed(1)}%`;


    updateSpending();
}


function updateSpending() {

    const spending = {};


    transactions.forEach(transaction => {

        if (transaction.type !== "expense") {
            return;
        }


        const category =
            transaction.category;


        if (!spending[category]) {
            spending[category] = 0;
        }


        spending[category] += Number(
            transaction.amount
        );

    });


    const container =
        document.getElementById(
            "spending"
        );


    const categories =
        Object.entries(spending)
        .sort((a, b) => b[1] - a[1]);


    if (categories.length === 0) {

        container.innerHTML =
            "<p>No spending yet.</p>";

        return;
    }


    container.innerHTML =
        categories.map(
            ([category, amount]) => {

                return `
                    <div class="transaction">

                        <div class="transaction-info">
                            <strong>
                                ${category}
                            </strong>
                        </div>

                        <strong>
                            RM ${amount.toFixed(2)}
                        </strong>

                    </div>
                `;

            }
        ).join("");
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