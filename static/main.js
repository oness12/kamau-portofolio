document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".skill-fill").forEach(bar => {
    const level = bar.dataset.level;
    bar.style.width = level + "%";
  });
});
