document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("setup-form");
  const tabs = form.querySelectorAll(".tab");
  const nextBtn = document.getElementById("nextBtn");
  const prevBtn = document.getElementById("prevBtn");
  const submitBtn = document.getElementById("submitBtn");
  let currentTab = 0;

  function showTab(n) {
    tabs.forEach((tab, i) => tab.classList.toggle("active", i === n));
    prevBtn.style.display = n === 0 ? "none" : "inline-block";
    nextBtn.style.display = n === tabs.length - 1 ? "none" : "inline-block";
    submitBtn.style.display = n === tabs.length - 1 ? "inline-block" : "none";
  }

  function validateTab() {
    const inputs = tabs[currentTab].querySelectorAll("input, select");
    for (const input of inputs) {
      if (!input.checkValidity()) {
        input.reportValidity();
        return false;
      }
    }
    return true;
  }

  nextBtn.addEventListener("click", () => {
    if (!validateTab()) return;
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

  // Optional: let Enter key advance steps naturally
  form.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      e.preventDefault(); // prevent accidental form submit
      if (currentTab < tabs.length - 1) {
        if (validateTab()) {
          currentTab++;
          showTab(currentTab);
        }
      }
    }
  });

  showTab(currentTab); // initialize first tab
});
