document.addEventListener("DOMContentLoaded", function() {

    async function loadDashboardData() {
        try {
            const res = await fetch('/dashboard-data/');
            const data = await res.json();

            // ------------------------------
            // CALORIES
            // ------------------------------
            const eatenCalories = data.eaten_calories || 0;

            document.getElementById("eatenCalories").textContent = Math.round(eatenCalories);
            document.getElementById("remainingCalories").textContent = Math.round(data.remaining_calories);

            const caloriePercent = data.daily_calories > 0
                ? (eatenCalories / data.daily_calories) * 100
                : 0;

            document.getElementById("calorieProgress").style.width = `${caloriePercent}%`;


            // ------------------------------
            // MACROS
            // ------------------------------

            // PROTEIN
            document.getElementById("proteinEaten").textContent = Math.round(data.protein_total);
            document.getElementById("proteinRemaining").textContent = Math.round(data.protein_remaining);

            document.getElementById("proteinBar").style.width =
                `${Math.min((data.protein_total / data.protein_goal) * 100, 100)}%`;


            // CARBS
            document.getElementById("carbsEaten").textContent = Math.round(data.carbs_total);
            document.getElementById("carbsRemaining").textContent = Math.round(data.carbs_remaining);

            document.getElementById("carbBar").style.width =
                `${Math.min((data.carbs_total / data.carbs_goal) * 100, 100)}%`;


            // FATS
            document.getElementById("fatsEaten").textContent = Math.round(data.fats_total);
            document.getElementById("fatsRemaining").textContent = Math.round(data.fats_remaining);

            document.getElementById("fatBar").style.width =
                `${Math.min((data.fats_total / data.fats_goal) * 100, 100)}%`;

        } catch (error) {
            console.error('Error fetching dashboard data:', error);
        }
    }

    loadDashboardData();

    // ------------------------------
    // ADD MEAL
    // ------------------------------
    const addMealForm = document.getElementById("addMealForm");

    if (addMealForm) {
        addMealForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(addMealForm);

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
});
