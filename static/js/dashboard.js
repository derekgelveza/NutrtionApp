// dashboard.js
document.addEventListener("DOMContentLoaded", () => {

  function formatDate(dateObj) {
    return dateObj.toISOString().slice(0, 10); 
  }

  function getCookie(name) {

    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }

  function getCSRFToken() {

    const cookie = getCookie('csrftoken');
    if (cookie) return cookie;
    const el = document.querySelector("[name=csrfmiddlewaretoken]");
    return el ? el.value : "";
  }

  function numberOrZero(v) {
    const n = Number(v);
    return Number.isFinite(n) ? n : 0;
  }


  let currentDate = new Date();
  let mealsCache = []; 


  const selectedDateSpan = document.getElementById("selectedDate");
  const prevBtn = document.getElementById("prevDay");
  const nextBtn = document.getElementById("nextDay");


  const eatenCaloriesEl = document.getElementById("eatenCalories");
  const remainingCaloriesEl = document.getElementById("remainingCalories");
  const calorieProgressEl = document.getElementById("calorieProgress");

  const proteinEatenEl = document.getElementById("proteinEaten");
  const proteinRemainingEl = document.getElementById("proteinRemaining");
  const proteinBarEl = document.getElementById("proteinBar");

  const carbsEatenEl = document.getElementById("carbsEaten");
  const carbsRemainingEl = document.getElementById("carbsRemaining");
  const carbBarEl = document.getElementById("carbBar");

  const fatsEatenEl = document.getElementById("fatsEaten");
  const fatsRemainingEl = document.getElementById("fatsRemaining");
  const fatBarEl = document.getElementById("fatBar");


  const mealsContainer = document.getElementById("mealsContainer");

  const openAddModalBtn = document.getElementById("openAddModal");


  const mealModal = document.getElementById("mealModal"); 
  const modalTitle = document.getElementById("modalTitle");
  const mealForm = document.getElementById("mealForm");
  const mealIdInput = document.getElementById("mealId");
  const mealNameInput = document.getElementById("mealName");
  const mealCaloriesInput = document.getElementById("mealCalories");
  const mealProteinInput = document.getElementById("mealProtein");
  const mealCarbsInput = document.getElementById("mealCarbs");
  const mealFatsInput = document.getElementById("mealFats");
  const closeModalBtn = document.getElementById("closeModal");


  function updateDisplayedDate() {
    selectedDateSpan.textContent = currentDate.toLocaleDateString("en-US", {
      month: "long",
      day: "numeric",
      year: "numeric",
    });
  }

  function showModal(mode = "add", meal = null) {

    if (mode === "add") {
      modalTitle.textContent = "Add Meal";
      mealIdInput.value = "";
      mealForm.reset();
    } else {
      modalTitle.textContent = "Edit Meal";
      mealIdInput.value = meal.id || "";
      mealNameInput.value = meal.name || "";
      mealCaloriesInput.value = meal.calories ?? "";
      mealProteinInput.value = meal.protein ?? "";
      mealCarbsInput.value = meal.carbs ?? "";
      mealFatsInput.value = meal.fats ?? "";
    }
    mealModal.classList.remove("hidden");

    setTimeout(() => mealNameInput.focus(), 60);
  }

  function hideModal() {
    mealModal.classList.add("hidden");
  }

  function renderMealsList(meals) {
    mealsContainer.innerHTML = "";
    if (!meals || meals.length === 0) {
      const li = document.createElement("li");
      li.textContent = "No meals logged for this day.";
      mealsContainer.appendChild(li);
      return;
    }

    meals.forEach((meal) => {
      const li = document.createElement("li");
      li.className = "meal-row";

      li.innerHTML = `
        <div class="meal-info">
          <strong class="meal-name">${escapeHtml(meal.name)}</strong>
          <div class="meal-macros">
            ${Math.round(meal.calories)} kcal |
            P: ${Math.round(meal.protein)}g
            C: ${Math.round(meal.carbs)}g
            F: ${Math.round(meal.fats)}g
          </div>
        </div>
        <div class="meal-actions">
          <button class="btn-small edit-btn" data-id="${meal.id}" title="Edit">✏️</button>
          <button class="btn-small delete-btn" data-id="${meal.id}" title="Delete">🗑️</button>
        </div>
      `;
      mealsContainer.appendChild(li);
    });

    attachMealEventListeners();
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


  function attachMealEventListeners() {

    const editButtons = mealsContainer.querySelectorAll(".edit-btn");
    editButtons.forEach((btn) =>
      btn.addEventListener("click", (e) => {
        const id = e.currentTarget.dataset.id;
        const meal = mealsCache.find((m) => String(m.id) === String(id));
        if (!meal) {
          alert("Meal not found.");
          return;
        }
        showModal("edit", meal);
      })
    );


    const delButtons = mealsContainer.querySelectorAll(".delete-btn");
    delButtons.forEach((btn) =>
      btn.addEventListener("click", async (e) => {
        const id = e.currentTarget.dataset.id;
        if (!confirm("Delete this meal?")) return;
        try {
          const res = await fetch(`/delete-meal/${id}/`, {
            method: "DELETE",
            headers: {
              "X-CSRFToken": getCSRFToken(),
            },
          });
          const json = await res.json();
          if (json.success) {
            await loadDashboardData();
          } else {
            console.error("Delete failed:", json);
            alert("Could not delete meal.");
          }
        } catch (err) {
          console.error("Delete error:", err);
          alert("Delete request failed.");
        }
      })
    );
  }


  async function loadDashboardData() {
    try {
      const dateString = formatDate(currentDate);
      const res = await fetch(`/dashboard-data/?date=${dateString}`);
      if (!res.ok) {
        console.error("dashboard-data returned", res.status);
        return;
      }
      const data = await res.json();


      const eatenCalories = numberOrZero(data.eaten_calories);
      const dailyCalories = numberOrZero(data.daily_calories);

      eatenCaloriesEl.textContent = Math.round(eatenCalories);
      remainingCaloriesEl.textContent = Math.round(numberOrZero(data.remaining_calories));

      const caloriePct = dailyCalories > 0 ? (eatenCalories / dailyCalories) * 100 : 0;
      calorieProgressEl.style.width = `${Math.min(caloriePct, 100)}%`;


      const proteinTotal = numberOrZero(data.protein_total);
      const proteinRemaining = numberOrZero(data.protein_remaining);
      proteinEatenEl.textContent = Math.round(proteinTotal);
      proteinRemainingEl.textContent = Math.round(proteinRemaining);
      proteinBarEl.style.width = `${Math.min(
        100,
        data.protein_goal ? (proteinTotal / data.protein_goal) * 100 : 0
      )}%`;


      const carbsTotal = numberOrZero(data.carbs_total);
      const carbsRemaining = numberOrZero(data.carbs_remaining);
      carbsEatenEl.textContent = Math.round(carbsTotal);
      carbsRemainingEl.textContent = Math.round(carbsRemaining);
      carbBarEl.style.width = `${Math.min(
        100,
        data.carbs_goal ? (carbsTotal / data.carbs_goal) * 100 : 0
      )}%`;


      const fatsTotal = numberOrZero(data.fats_total);
      const fatsRemaining = numberOrZero(data.fats_remaining);
      fatsEatenEl.textContent = Math.round(fatsTotal);
      fatsRemainingEl.textContent = Math.round(fatsRemaining);
      fatBarEl.style.width = `${Math.min(
        100,
        data.fats_goal ? (fatsTotal / data.fats_goal) * 100 : 0
      )}%`;


      mealsCache = Array.isArray(data.meals) ? data.meals : [];
      renderMealsList(mealsCache);
    } catch (err) {
      console.error("Error loading dashboard data:", err);
    }
  }


  mealForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = mealIdInput.value && mealIdInput.value.trim() !== "" ? mealIdInput.value : null;
    const payload = {
      name: mealNameInput.value.trim(),
      calories: Number(mealCaloriesInput.value) || 0,
      protein: Number(mealProteinInput.value) || 0,
      carbs: Number(mealCarbsInput.value) || 0,
      fats: Number(mealFatsInput.value) || 0,
      date: formatDate(currentDate), 
      meal_type: document.getElementById("mealType").value
    };


    if (!payload.name) {
      alert("Please enter a name for the meal.");
      mealNameInput.focus();
      return;
    }

    try {
      const url = id ? `/edit-meal/${id}/` : `/add-meal/`;
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(payload),
      });

      const json = await res.json();
      if (json.success) {
        hideModal();

        await loadDashboardData();
      } else {
        console.error("Save failed:", json);
        alert("Could not save meal. Check console for details.");
      }
    } catch (err) {
      console.error("Save error:", err);
      alert("Error saving meal.");
    }
  });


  if (openAddModalBtn) {
    openAddModalBtn.addEventListener("click", () => showModal("add", null));
  }

  if (closeModalBtn) {
    closeModalBtn.addEventListener("click", hideModal);
  }


  if (mealModal) {
    mealModal.addEventListener("click", (e) => {
      if (e.target === mealModal) hideModal();
    });
  }


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


  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && mealModal && !mealModal.classList.contains("hidden")) {
      hideModal();
    }
  });


  updateDisplayedDate();
  loadDashboardData();
});
