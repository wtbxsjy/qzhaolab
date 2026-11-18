// Joins the two halves of the contact e-mail address (see layouts/partials/email.html).
document.querySelectorAll("a.js-email").forEach(function (a) {
  var address = a.dataset.u + "@" + a.dataset.d;
  a.href = "mailto:" + address;
  a.textContent = address;
});
