document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector(".page");
  const themeToggle = document.getElementById("theme-toggle");
  const hamburger = document.getElementById("hamburger");
  const mobileMenu = document.getElementById("mobileMenu");

  /* Page fade-in */
  if (page) {
    requestAnimationFrame(() => {
      page.classList.add("loaded");
    });
  }

  /* Theme toggle */
  if (themeToggle) {
    const currentTheme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", currentTheme);

    themeToggle.addEventListener("click", () => {
      const newTheme =
        document.documentElement.getAttribute("data-theme") === "dark"
          ? "light"
          : "dark";
      document.documentElement.setAttribute("data-theme", newTheme);
      localStorage.setItem("theme", newTheme);
    });
  }

  /* Mobile menu */
  if (hamburger && mobileMenu) {
    hamburger.addEventListener("click", () => {
      mobileMenu.classList.toggle("open");
    });

    mobileMenu.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => {
        mobileMenu.classList.remove("open");
      });
    });
  }

  /* Skill bars animation */
  document.querySelectorAll(".skill-fill").forEach(bar => {
    const level = bar.getAttribute("data-level");
    if (level) {
      bar.style.width = level + "%";
    }
  });
});
