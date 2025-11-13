document.addEventListener("DOMContentLoaded", function() {

    // Function to load dashboard data and update UI
    async function loadDashboardData() {
        try {
            const res = await fetch('/dashboard-data/');
            const data = await res.json();

            // Set eaten and remaining calories
            const eatenCalories = data.eaten_calories || 0;
            const remainingCalories = data.daily_calories - eatenCalories;

            // Update DOM elements
            document.getElementById("eatenCalories").textContent = Math.round(eatenCalories);
            document.getElementById("remainingCalories").textContent = Math.round(remainingCalories); // <-- fixed variable name

            // Update progress bar
            const progressPercent = data.daily_calories > 0
                ? (eatenCalories / data.daily_calories) * 100
                : 0;
            const progressBar = document.getElementById("calorieProgress");
            progressBar.style.width = `${progressPercent}%`;

            // Doughnut chart
            const ctx = document.getElementById('macroChart').getContext('2d');
            if (window.macroChart) window.macroChart.destroy();

            window.macroChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Carbs', 'Protein', 'Fats'],
                    datasets: [{
                        data: [data.carbs, data.protein, data.fats],
                        backgroundColor: ['#ebdb5eff', '#b437e2ff', '#a2f09bff'],
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });

        } catch (error) {
            console.error('Error fetching dashboard data:', error);
        }
    }

    // Initial load
    loadDashboardData();

    // Add Meal Form AJAX logic
    const addMealForm = document.getElementById("addMealForm");
    if (addMealForm) {
        addMealForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(addMealForm);
            const csrfToken = formData.get("csrfmiddlewaretoken");

            try {
                const response = await fetch("/add_meal/", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken
                    },
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    addMealForm.reset();
                    // Refresh the dashboard data to update eaten/remaining calories
                    loadDashboardData();
                } else {
                    alert("Error adding meal: " + JSON.stringify(data.errors));
                }
            } catch (err) {
                console.error("Error adding meal:", err);
            }
        });
    }
});
