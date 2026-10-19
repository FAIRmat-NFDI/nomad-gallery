document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".use-case-card__toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const card = button.closest(".use-case-card");
      if (!card) return;

      const expanded = card.classList.toggle("is-expanded");
      const label = button.querySelector(".use-case-card__toggle-label");

      if (label) {
        label.textContent = expanded ? "Show Less" : "View Details";
      }

      button.setAttribute("aria-expanded", expanded ? "true" : "false");
    });
  });
});