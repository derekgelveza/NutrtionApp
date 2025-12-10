// fridgeAi.js
document.addEventListener("DOMContentLoaded", () => {
  // ---------- Helpers ----------
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  }

  function getCSRFToken() {
    const cookie = getCookie("csrftoken");
    if (cookie) return cookie;
    const el = document.querySelector("[name=csrfmiddlewaretoken]");
    return el ? el.value : "";
  }

  function escapeHtml(unsafe) {
    if (unsafe === null || unsafe === undefined) return "";
    return String(unsafe)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // ---------- DOM references ----------
  const ingredientsInput = document.getElementById("ingredientsInput");
  const generateBtn = document.getElementById("generateMealsBtn");
  const mealsContainer = document.getElementById("mealsContainer");
  const messageEl = document.getElementById("message");

  // ---------- UI helpers ----------
  function showMessage(msg, type = "info") {
    messageEl.textContent = msg;
    messageEl.className = type;
    messageEl.classList.remove("hidden");
  }

  function hideMessage() {
    messageEl.textContent = "";
    messageEl.className = "hidden";
  }

  function renderMeals(meals) {
    mealsContainer.innerHTML = "";

    if (!meals || meals.length === 0) {
      mealsContainer.innerHTML = "<li>No meal suggestions available.</li>";
      return;
    }

    meals.forEach((meal) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <strong>${escapeHtml(meal.name)}</strong> -
        ${meal.calories} kcal |
        P: ${meal.protein}g |
        C: ${meal.carbs}g |
        F: ${meal.fats}g
      `;
      mealsContainer.appendChild(li);
    });
  }

  // ---------- Event ----------
  generateBtn.addEventListener("click", async () => {
    const ingredients = ingredientsInput.value.trim();
    if (!ingredients) {
      showMessage("Please enter some ingredients.", "error");
      return;
    }

    hideMessage();
    showMessage("Generating meals...", "info");

    try {
      const res = await fetch("/fridge-ai/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ ingredients }),
      });

      const data = await res.json();

      if (res.ok && data.meals) {
        renderMeals(data.meals);
        hideMessage();
      } else {
        showMessage(data.error || "Failed to generate meals.", "error");
      }
    } catch (err) {
      console.error("Error generating meals:", err);
      showMessage("An error occurred. Check console for details.", "error");
    }
  });
});
