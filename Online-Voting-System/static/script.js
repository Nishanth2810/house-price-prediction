// script.js - small helpers: dark mode, logout confirmation, and search filter
document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.getElementById('dark-toggle');
  if (toggle) {
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      document.body.classList.toggle('dark');
      toggle.textContent = document.body.classList.contains('dark') ? 'Light' : 'Dark';
    });
  }

  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', function (e) {
      if (!confirm('Are you sure you want to logout?')) e.preventDefault();
    });
  }
});
