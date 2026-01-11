// Page fade-in
document.addEventListener("DOMContentLoaded", () => {
  document.querySelector(".page")?.classList.add("loaded");
});

// Skill bars (if present)
document.querySelectorAll(".skill-fill").forEach(bar => {
  const level = bar.dataset.level;
  if (level) bar.style.width = level + "%";
});
