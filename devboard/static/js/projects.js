/* ============================================================
   DevBoard — projects.js
   Filters project cards on the Projects page by status
   (All / In Progress / Completed / Planned) without a page reload.
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
  const filterButtons = document.querySelectorAll('#projectFilters .db-filter-pill');
  const projectItems = document.querySelectorAll('.project-item');
  const noResultsMsg = document.getElementById('noResultsMsg');

  if (!filterButtons.length) return;

  filterButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      filterButtons.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');
      let visibleCount = 0;

      projectItems.forEach(function (item) {
        const matches = (filter === 'all' || item.getAttribute('data-status') === filter);
        item.classList.toggle('d-none', !matches);
        if (matches) visibleCount++;
      });

      if (noResultsMsg) {
        noResultsMsg.classList.toggle('d-none', visibleCount !== 0);
      }
    });
  });
});
