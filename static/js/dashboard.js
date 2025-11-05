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
                      backgroundColor: ['#f4a261', '#2a9d8f', '#e76f51'],
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
