document.addEventListener("DOMContentLoaded", function() {
    fetch('/dashboard-data/')
      .then(res => res.json())
      .then(data => {
        const progressPercent = (data.eaten_calories / data.daily_calories) * 100;

        document.getElementById("eatenCalories").textContent = Math.round(data.eaten_calories);
        document.getElementById("remainingCalories").textContent = Math.round(data.remaining_calories);

        const progressBar = document.getElementById("calorieProgress");
        progressBar.style.width = `${progressPercent}%`;


          const ctx = document.getElementById('macroChart').getContext('2d');
          new Chart(ctx, {
              type: 'doughnut',
              data: {
                  labels: ['Carbs', 'Protein', 'Fats'],
                  datasets: [{
                      data: [data.carbs, data.protein, data.fats],
                      backgroundColor: ['#ebdb5eff', '#b437e2ff', '#a2f09bff'],
                      
                  }]
              },
              options: {
                  responsive: true,
                  plugins: {
                      legend: { position: 'bottom' }
                  }
              }
          });
      })
      .catch(error => console.error('Error fetching dashboard data:', error));
});
