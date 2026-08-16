/* ============================================================
   DevBoard — charts.js
   Renders every Chart.js visualisation used in DevBoard:
     - #weeklyChart   bar chart  (dashboard + analytics)
     - #statusChart   doughnut   (analytics: todo/in-progress/done)
     - #progressChart horizontal bar (analytics: progress per project)
   Each render is guarded by a canvas-existence check so this one
   file can be safely included on any page — it only draws what's
   actually present in that page's HTML.
   Expects globals set by an inline <script> block in the template:
   WEEKLY_LABELS, WEEKLY_COUNTS, and (analytics only) STATUS_BREAKDOWN,
   PROJECT_PROGRESS — all built from real Task/Project data in Django.
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
  const commonGridColor = 'rgba(255,255,255,0.06)';
  const commonTickColor = '#8b8b98';
  const tooltipStyle = {
    backgroundColor: '#1c1c24',
    borderColor: 'rgba(255,255,255,0.1)',
    borderWidth: 1,
    padding: 10,
  };

  // ---------- Weekly productivity (bar) ----------
  const weeklyCanvas = document.getElementById('weeklyChart');
  if (weeklyCanvas && typeof Chart !== 'undefined' && typeof WEEKLY_LABELS !== 'undefined') {
    const gradient = weeklyCanvas.getContext('2d').createLinearGradient(0, 0, 0, 260);
    gradient.addColorStop(0, 'rgba(239, 68, 82, 0.9)');
    gradient.addColorStop(1, 'rgba(139, 92, 246, 0.9)');

    new Chart(weeklyCanvas, {
      type: 'bar',
      data: {
        labels: WEEKLY_LABELS,
        datasets: [{
          label: 'Tasks completed',
          data: WEEKLY_COUNTS,
          backgroundColor: gradient,
          borderRadius: 6,
          maxBarThickness: 42,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false }, tooltip: tooltipStyle },
        scales: {
          y: { beginAtZero: true, ticks: { color: commonTickColor, stepSize: 1, font: { size: 11 } }, grid: { color: commonGridColor } },
          x: { ticks: { color: commonTickColor, font: { size: 12 } }, grid: { display: false } },
        },
      },
    });
  }

  // ---------- Task status breakdown (doughnut) ----------
  const statusCanvas = document.getElementById('statusChart');
  if (statusCanvas && typeof Chart !== 'undefined' && typeof STATUS_BREAKDOWN !== 'undefined') {
    new Chart(statusCanvas, {
      type: 'doughnut',
      data: {
        labels: ['Todo', 'In Progress', 'Completed'],
        datasets: [{
          data: [STATUS_BREAKDOWN.todo, STATUS_BREAKDOWN.in_progress, STATUS_BREAKDOWN.completed],
          backgroundColor: ['#5c5c68', '#8b5cf6', '#ef4452'],
          borderColor: '#17171d',
          borderWidth: 3,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '68%',
        plugins: {
          legend: { position: 'bottom', labels: { color: commonTickColor, boxWidth: 10, font: { size: 12 } } },
          tooltip: tooltipStyle,
        },
      },
    });
  }

  // ---------- Project progress (horizontal bar) ----------
  const progressCanvas = document.getElementById('progressChart');
  if (progressCanvas && typeof Chart !== 'undefined' && typeof PROJECT_PROGRESS !== 'undefined') {
    new Chart(progressCanvas, {
      type: 'bar',
      data: {
        labels: PROJECT_PROGRESS.map(p => p.name),
        datasets: [{
          label: 'Progress %',
          data: PROJECT_PROGRESS.map(p => p.progress),
          backgroundColor: 'rgba(139, 92, 246, 0.75)',
          borderRadius: 6,
          maxBarThickness: 26,
        }],
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false }, tooltip: tooltipStyle },
        scales: {
          x: { min: 0, max: 100, ticks: { color: commonTickColor, font: { size: 11 } }, grid: { color: commonGridColor } },
          y: { ticks: { color: commonTickColor, font: { size: 12 } }, grid: { display: false } },
        },
      },
    });
  }
});
