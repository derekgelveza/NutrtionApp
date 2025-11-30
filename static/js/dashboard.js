document.addEventListener("DOMContentLoaded", function () {

    let currentDate = new Date(); // start at today

    function formatDate(dateObj) {
        return dateObj.toISOString().slice(0, 10); // YYYY-MM-DD
    }

    function updateDisplayedDate() {
        const currentDateSpan = document.getElementById("selectedDate");
        currentDateSpan.textContent = currentDate.toLocaleDateString("en-US", {
            month: "long",
            day: "numeric",
            year: "numeric"
        });
    }

    async function loadDashboardData() {
        try {
            const dateString = formatDate(currentDate);

            const res = await fetch(`/dashboard-data/?date=${dateString}`);
            const data = await res.json();

            // CALORIES
            const eatenCalories = data.eaten_calories || 0;

            document.getElementById("eatenCalories").textContent = Math.round(eatenCalories);
            document.getElementById("remainingCalories").textContent =
                Math.round(data.remaining_calories);

            const caloriePercent =
                data.daily_calories > 0
                    ? (eatenCalories / data.daily_calories) * 100
                    : 0;

            document.getElementById("calorieProgress").style.width =
                `${Math.min(caloriePercent, 100)}%`;

            // PROTEIN
            document.getElementById("proteinEaten").textContent =
                Math.round(data.protein_total);
            document.getElementById("proteinRemaining").textContent =
                Math.round(data.protein_remaining);

            document.getElementById("proteinBar").style.width =
                `${Math.min((data.protein_total / data.protein_goal) * 100, 100)}%`;

            // CARBS
            document.getElementById("carbsEaten").textContent =
                Math.round(data.carbs_total);
            document.getElementById("carbsRemaining").textContent =
                Math.round(data.carbs_remaining);

            document.getElementById("carbBar").style.width =
                `${Math.min((data.carbs_total / data.carbs_goal) * 100, 100)}%`;

            // FATS
            document.getElementById("fatsEaten").textContent =
                Math.round(data.fats_total);
            document.getElementById("fatsRemaining").textContent =
                Math.round(data.fats_remaining);

            document.getElementById("fatBar").style.width =
                `${Math.min((data.fats_total / data.fats_goal) * 100, 100)}%`;

        } catch (error) {
            console.error("Error fetching dashboard data:", error);
        }
    }

    // PREVIOUS / NEXT DAY BUTTONS
    const prevBtn = document.getElementById("prevDay");
    const nextBtn = document.getElementById("nextDay");

    if (prevBtn) {
        prevBtn.addEventListener("click", () => {
            currentDate.setDate(currentDate.getDate() - 1);
            updateDisplayedDate();
            loadDashboardData();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", () => {
            currentDate.setDate(currentDate.getDate() + 1);
            updateDisplayedDate();
            loadDashboardData();
        });
    }

    // ADD MEAL — Uses selected date
    const addMealForm = document.getElementById("addMealForm");

    if (addMealForm) {
        addMealForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(addMealForm);
            formData.append("date", formatDate(currentDate)); // send selected date

            try {
                const response = await fetch("/add-meal/", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": formData.get("csrfmiddlewaretoken")
                    },
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    addMealForm.reset();
                    loadDashboardData();
                } else {
                    alert("Error adding meal.");
                }

            } catch (err) {
                console.error("Error adding meal:", err);
            }
        });
    }

    // INITIAL LOAD
    updateDisplayedDate();
    loadDashboardData();

});
