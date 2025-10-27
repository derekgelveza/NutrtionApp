document.addEventListener("DOMContentLoaded", () => {
  // Determine which form is on the page
  const registrationForm = document.getElementById("registration-form");
  const setupForm = document.getElementById("setup-form");
  let form = registrationForm || setupForm;
  if (!form) return; // No relevant form on this page

  const tabs = form.querySelectorAll(".tab");
  const nextBtn = document.getElementById("nextBtn");
  const prevBtn = document.getElementById("prevBtn");
  let currentTab = 0;

  showTab(currentTab);

  function showTab(n) {
    tabs.forEach((tab, i) => tab.classList.toggle("active", i === n));
    prevBtn.style.display = n === 0 ? "none" : "inline-block";

    // Change Next button text
    nextBtn.textContent = n === tabs.length - 1 ? "Submit" : "Next";

    // Change type of nextBtn to "submit" only on last tab
    nextBtn.type = n === tabs.length - 1 ? "submit" : "button";
  }

  nextBtn.addEventListener("click", (e) => {
    // Basic validation for inputs in current tab
    const inputs = tabs[currentTab].querySelectorAll("input, select");
    for (const input of inputs) {
      if (!input.checkValidity()) {
        input.reportValidity();
        return;
      }
    }

    // Password validation for registration form
    if (registrationForm && currentTab === tabs.length - 1) {
      const passwordInput = form.querySelector("#password");
      const confirmInput = form.querySelector("#confirm-password");
      const errorMsg = form.querySelector("#password-error");

      if (passwordInput && confirmInput) {
        const password = passwordInput.value;
        const confirm = confirmInput.value;
        const strongPassword = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;

        if (!strongPassword.test(password) || password !== confirm) {
          if (errorMsg) errorMsg.style.display = "block";
          e.preventDefault();
          return;
        } else {
          if (errorMsg) errorMsg.style.display = "none";
        }
      }
    }

    // Move to next tab if not last
    if (currentTab < tabs.length - 1) {
      currentTab++;
      showTab(currentTab);
    }
  });

  prevBtn.addEventListener("click", () => {
    if (currentTab > 0) {
      currentTab--;
      showTab(currentTab);
    }
  });
});
