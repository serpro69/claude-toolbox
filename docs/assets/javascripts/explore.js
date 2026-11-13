/* Explore page (docs/overrides/explore.html). Progressive enhancement only: the page is
   complete without this script. It reveals each chapter's excerpt as the chapter reaches
   the middle of the viewport and keeps #<chapter-id> in the URL so a position can be shared. */
(function () {
  var chapters = Array.prototype.slice.call(document.querySelectorAll('.xp-chapter'));
  if (!chapters.length) return;
  document.documentElement.classList.add('xp-js');

  if (!('IntersectionObserver' in window)) {
    chapters.forEach(function (chapter) { chapter.classList.add('is-active'); });
    return;
  }

  // Only rewrite the hash after the reader scrolls, so loading /explore/#symlink keeps its hash.
  var readerScrolled = false;
  ['wheel', 'touchmove', 'keydown'].forEach(function (type) {
    window.addEventListener(type, function () { readerScrolled = true; }, { passive: true, once: true });
  });

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var chapter = entry.target;
      chapter.classList.add('is-active');
      if (readerScrolled && location.hash !== '#' + chapter.id) {
        history.replaceState(null, '', '#' + chapter.id);
      }
    });
  }, { rootMargin: '-45% 0px -45% 0px' });

  chapters.forEach(function (chapter) { observer.observe(chapter); });
})();
