/* ============================================================
   DevBoard — settings.js
   1. Instantly previews dark/light mode when the switch is toggled
      (the actual preference is saved to the database once the
      "Save Appearance" button submits the form to Django).
   2. Adds Bootstrap's form-control class to Django's built-in
      PasswordChangeForm fields, which don't carry it by default.
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
  // --- Live dark/light preview ---
  const darkModeSwitch = document.querySelector('input[name="dark_mode"]');
  if (darkModeSwitch) {
    darkModeSwitch.addEventListener('change', function () {
      document.body.classList.toggle('light-mode', !darkModeSwitch.checked);
    });
  }

  // --- Style Django's default auth form widgets to match DevBoard ---
  document.querySelectorAll('input[name="old_password"], input[name="new_password1"], input[name="new_password2"]')
    .forEach(function (input) {
      input.classList.add('form-control');
    });
});
