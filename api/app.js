// Wait for DOM to load
document.addEventListener("DOMContentLoaded", () => {
  const menu = document.getElementById("navbar-menu");
  const toggle = document.getElementById("mobile-menu");

  // Toggle mobile menu
  toggle.addEventListener("click", () => {
      const expanded = toggle.getAttribute("aria-expanded") === "true" || false;

      menu.classList.toggle("active");
      toggle.setAttribute("aria-expanded", !expanded);
  });

  // Optional: close menu when clicking outside on mobile
  document.addEventListener("click", (e) => {
      const isClickInside = toggle.contains(e.target) || menu.contains(e.target);
      if (!isClickInside && menu.classList.contains("active")) {
          menu.classList.remove("active");
          toggle.setAttribute("aria-expanded", "false");
      }
  });
});