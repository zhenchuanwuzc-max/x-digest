(function () {
  function mark() {
    var hash = location.hash || '';
    document.querySelectorAll('.nav a[href^="#"], .mob a[href^="#"]').forEach(function (a) {
      var on = hash && a.getAttribute('href') === hash;
      a.classList.toggle('is-current', on);
      if (on) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
  }
  window.addEventListener('hashchange', mark);
  mark();
})();
