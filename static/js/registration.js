document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".tab");
  const nextBtn = document.getElementById("nextBtn");
  const prevBtn = document.getElementById("prevBtn");
  let currentTab = 0;

  showTab(currentTab);

  function showTab(n) {
    tabs.forEach((tab, i) => tab.classList.toggle("active", i === n));
    prevBtn.style.display = n === 0 ? "none" : "inline-block";
    nextBtn.textContent = n === tabs.length - 1 ? "Submit" : "Next";
  }

  nextBtn.addEventListener("click", () => {
    // Basic validation for inputs in current tab
    const inputs = tabs[currentTab].querySelectorAll("input, select");
    for (const input of inputs) {
      if (!input.checkValidity()) {
        input.reportValidity();
        return;
      }
    }

    // Password validation (only if password field exists in this tab)
    const passwordInput = tabs[currentTab].querySelector("#password");
    if (passwordInput) {
      const password = document.getElementById("password").value;
      const confirm = document.getElementById("confirm-password").value;
      const errorMsg = document.getElementById("password-error");

      // Updated regex — requires at least 8 characters
      const strongPassword = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;
      const isValid = strongPassword.test(password);

      if (!isValid || password !== confirm) {
        errorMsg.style.display = "block";
        return;
      } else {
        errorMsg.style.display = "none";
      }
    }

    // Move to next tab or submit form
    if (currentTab < tabs.length - 1) {
      currentTab++;
      showTab(currentTab);
    } else {
      document.getElementById("registration-form").submit();
    }
  });

  prevBtn.addEventListener("click", () => {
    if (currentTab > 0) {
      currentTab--;
      showTab(currentTab);
    }
  });
});