/* ============================================================
   DevBoard — script.js
   Shared behaviour used on every page: mobile sidebar toggle.
   Page-specific logic (filters, charts, search) lives in its own
   file (projects.js, tasks.js, charts.js, settings.js) so nothing
   is loaded on a page that doesn't need it.
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
  const sidebar = document.getElementById('dbSidebar');
  const overlay = document.getElementById('dbOverlay');
  const toggleBtn = document.getElementById('dbSidebarToggle');

  if (toggleBtn && sidebar && overlay) {
    toggleBtn.addEventListener('click', function () {
      sidebar.classList.toggle('show');
      overlay.classList.toggle('show');
    });

    overlay.addEventListener('click', function () {
      sidebar.classList.remove('show');
      overlay.classList.remove('show');
    });

    // Close the mobile sidebar automatically after navigating
    sidebar.querySelectorAll('a.db-nav-link').forEach(function (link) {
      link.addEventListener('click', function () {
        sidebar.classList.remove('show');
        overlay.classList.remove('show');
      });
    });
  }

  // Auto-dismiss alert messages after a few seconds
  document.querySelectorAll('.alert').forEach(function (alertEl) {
    setTimeout(function () {
      alertEl.style.transition = 'opacity 0.4s ease';
      alertEl.style.opacity = '0';
      setTimeout(function () { alertEl.remove(); }, 400);
    }, 4500);
  });
});
