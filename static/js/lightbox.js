// Click a news picture to view it large. Arrow keys or the side buttons move between
// pictures of the same news item; Esc, the close button or a click outside closes it.
// Without this script, the thumbnail link simply opens the large image.
(function () {
  var dialog = document.getElementById("lightbox");
  if (!dialog || typeof dialog.showModal !== "function") return;
  var img = dialog.querySelector("img");
  var caption = dialog.querySelector("figcaption");
  var prev = dialog.querySelector(".prev");
  var next = dialog.querySelector(".next");
  var group = [];
  var index = 0;

  function show(i) {
    index = (i + group.length) % group.length;
    var link = group[index];
    var thumb = link.querySelector("img");
    img.src = link.href;
    img.alt = thumb ? thumb.alt : "";
    caption.textContent = link.dataset.caption || "";
    caption.hidden = !link.dataset.caption;
    prev.hidden = next.hidden = group.length < 2;
  }

  document.addEventListener("click", function (e) {
    var link = e.target.closest("a.news-thumb");
    if (!link) return;
    e.preventDefault();
    group = Array.prototype.slice.call(link.closest(".news-images").querySelectorAll("a.news-thumb"));
    show(group.indexOf(link));
    dialog.showModal();
  });

  prev.addEventListener("click", function () { show(index - 1); });
  next.addEventListener("click", function () { show(index + 1); });
  dialog.querySelector(".lightbox-close").addEventListener("click", function () { dialog.close(); });
  dialog.addEventListener("click", function (e) { if (e.target === dialog) dialog.close(); });
  dialog.addEventListener("keydown", function (e) {
    if (group.length < 2) return;
    if (e.key === "ArrowLeft") show(index - 1);
    if (e.key === "ArrowRight") show(index + 1);
  });
  dialog.addEventListener("close", function () { img.removeAttribute("src"); });
})();
