document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("setup-form");

    form.addEventListener("submit", (e) => {
        const mealsInput = document.getElementById("meals_per_day");
        if (mealsInput.value < 1) {
            e.preventDefault();
            alert("Number of meals must be at least 1.");
            mealsInput.focus();
        }
    });
});
