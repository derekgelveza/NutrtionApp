document.addEventListener("DOMContentLoaded", function() {
    fetch('/dashboard-data/')
      .then(res => res.json())
      .then(data => {
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
