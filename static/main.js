document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.getElementById("hamburger");
  const sidebar = document.getElementById("sidebar");

  if (hamburger && sidebar) {
    hamburger.addEventListener("click", () => {
      sidebar.classList.toggle("open");
    });
  }

  // Skill bars animation
  document.querySelectorAll(".skill-fill").forEach(bar => {
    const level = bar.getAttribute("data-level");
    bar.style.width = level + "%";
  });
});
