/* ============================================================
   DevBoard — tasks.js
   Search + status filtering for the Tasks page. Runs entirely in
   the browser against the tasks already rendered by Django, so
   filtering feels instant. Add / complete / delete still POST to
   Django (see the <form> elements in tasks.html).
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('taskSearch');
  const filterButtons = document.querySelectorAll('#taskList ~ * .db-filter-pill, .db-filter-pill');
  const taskRows = document.querySelectorAll('#taskList .db-task-row');
  const noResults = document.getElementById('noTaskResults');

  let activeFilter = 'all';

  function applyFilters() {
    const query = (searchInput ? searchInput.value.trim().toLowerCase() : '');
    let visibleCount = 0;

    taskRows.forEach(function (row) {
      const matchesFilter = (activeFilter === 'all' || row.getAttribute('data-status') === activeFilter);
      const matchesSearch = row.getAttribute('data-title').includes(query);
      const visible = matchesFilter && matchesSearch;
      row.classList.toggle('d-none', !visible);
      if (visible) visibleCount++;
    });

    if (noResults) {
      noResults.classList.toggle('d-none', visibleCount !== 0 || taskRows.length === 0);
    }
  }

  document.querySelectorAll('.db-filter-pill').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.db-filter-pill').forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      activeFilter = btn.getAttribute('data-filter');
      applyFilters();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', applyFilters);
  }
});
