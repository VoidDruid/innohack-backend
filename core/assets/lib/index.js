import Chart from 'chart.js';

export function siteEventChart(chartData) {
  return () => {
      const ctx = document.getElementById('SiteEventsDateChart').getContext('2d');

      // Parse the dates to JS
      chartData.forEach((d) => {
        d.x = new Date(d.date);
      });

      // Render the chart
      const chart = new Chart(ctx, {
        type: 'bar',
        data: {
          datasets: [
            {
              label: 'Происшествия',
              data: chartData,
              backgroundColor: 'rgba(220,20,20,0.5)',
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            xAxes: [
              {
                type: 'time',
                time: {
                  unit: 'day',
                  round: 'day',
                  displayFormats: {
                    day: 'MMM D',
                  },
                },
              },
            ],
            yAxes: [
              {
                ticks: {
                  beginAtZero: true,
                },
              },
            ],
          },
        },
      });
  };
}


export function siteWorkersChart(chartData) {
  return () => {
      const ctx = document.getElementById('SiteWorkersDateChart').getContext('2d');

      // Parse the dates to JS
      chartData.forEach((d) => {
        d.x = new Date(d.date);
      });

      // Render the chart
      const chart = new Chart(ctx, {
        type: 'bar',
        data: {
          datasets: [
            {
              label: 'Рабочие',
              data: chartData,
              backgroundColor: 'rgba(220,20,20,0.5)',
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            xAxes: [
              {
                type: 'time',
                time: {
                  unit: 'day',
                  round: 'day',
                  displayFormats: {
                    day: 'MMM D',
                  },
                },
              },
            ],
            yAxes: [
              {
                ticks: {
                  beginAtZero: true,
                },
              },
            ],
          },
        },
      });
  };
}