document.addEventListener("DOMContentLoaded", () => {

  // Skills animation
  document.querySelectorAll(".skill-fill").forEach(bar => {
    bar.style.width = bar.dataset.level + "%";
  });

  // Mobile menu
  const hamburger = document.getElementById("hamburger");
  const menu = document.getElementById("mobileMenu");

  if (hamburger) {
    hamburger.addEventListener("click", () => {
      menu.classList.toggle("open");
    });
  }

  // Pie chart
  const ctx = document.getElementById("analyticsPieChart");
  if (ctx) {
    new Chart(ctx, {
      type:"pie",
      data:{
        labels:["Cleaning","EDA","Visualization","Reporting","SQL"],
        datasets:[{
          data:[30,25,20,15,10],
          backgroundColor:["#5c7cfa","#4dabf7","#63e6be","#ffd43b","#ff8787"]
        }]
      }
    });
  }

});
