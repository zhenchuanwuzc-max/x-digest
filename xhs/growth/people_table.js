(function () {
  var root = document.getElementById('people-toolbar');
  var table = document.querySelector('table.cmp');
  if (!root || !table) return;
  var tbody = table.tBodies[0];
  var rows = Array.prototype.slice.call(tbody.rows);
  var status = document.getElementById('people-status');
  var empty = document.getElementById('people-empty');
  var state = { sort: 'ord', dir: 1, lang: 'all', tags: {} };

  function parseNum(v) {
    if (v === '' || v == null) return null;
    var n = Number(v);
    return isFinite(n) ? n : null;
  }

  function visible(row) {
    if (state.lang === 'zh' && row.getAttribute('data-lang') !== 'zh') return false;
    var selected = Object.keys(state.tags).filter(function (k) { return state.tags[k]; });
    if (!selected.length) return true;
    var have = (row.getAttribute('data-audience') || '').split(/\s+/).filter(Boolean);
    for (var i = 0; i < selected.length; i++) {
      if (have.indexOf(selected[i]) !== -1) return true;
    }
    return false;
  }

  function cmp(a, b) {
    if (state.sort === 'ord') {
      return Number(a.getAttribute('data-ord')) - Number(b.getAttribute('data-ord'));
    }
    var ka = parseNum(a.getAttribute('data-' + state.sort));
    var kb = parseNum(b.getAttribute('data-' + state.sort));
    var aU = ka == null, bU = kb == null;
    if (aU && bU) return Number(a.getAttribute('data-ord')) - Number(b.getAttribute('data-ord'));
    if (aU) return 1;
    if (bU) return -1;
    if (ka !== kb) return (ka - kb) * state.dir;
    return Number(a.getAttribute('data-ord')) - Number(b.getAttribute('data-ord'));
  }

  function apply() {
    var sorted = rows.slice().sort(cmp);
    var shown = 0;
    sorted.forEach(function (r) {
      var on = visible(r);
      r.hidden = !on;
      if (on) {
        tbody.appendChild(r);
        shown++;
      }
    });
    // keep hidden rows in DOM after visible ones for stable re-filter
    sorted.forEach(function (r) { if (r.hidden) tbody.appendChild(r); });
    if (status) status.textContent = '显示 ' + shown + ' / ' + rows.length + ' 人';
    if (empty) empty.hidden = shown !== 0;
    syncButtons();
  }

  function syncButtons() {
    root.querySelectorAll('[data-sort]').forEach(function (btn) {
      var on = btn.getAttribute('data-sort') === state.sort && Number(btn.getAttribute('data-dir') || 1) === state.dir;
      if (btn.getAttribute('data-sort') === 'ord') on = state.sort === 'ord';
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.classList.toggle('on', on);
    });
    root.querySelectorAll('[data-lang]').forEach(function (btn) {
      var on = btn.getAttribute('data-lang') === state.lang;
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.classList.toggle('on', on);
    });
    root.querySelectorAll('[data-tag]').forEach(function (btn) {
      var on = !!state.tags[btn.getAttribute('data-tag')];
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.classList.toggle('on', on);
    });
  }

  root.addEventListener('click', function (ev) {
    var btn = ev.target.closest('button');
    if (!btn || !root.contains(btn)) return;
    if (btn.hasAttribute('data-sort')) {
      state.sort = btn.getAttribute('data-sort');
      state.dir = Number(btn.getAttribute('data-dir') || 1);
      apply();
      return;
    }
    if (btn.hasAttribute('data-lang')) {
      state.lang = btn.getAttribute('data-lang');
      apply();
      return;
    }
    if (btn.hasAttribute('data-tag')) {
      var t = btn.getAttribute('data-tag');
      state.tags[t] = !state.tags[t];
      apply();
      return;
    }
    if (btn.hasAttribute('data-clear')) {
      state = { sort: 'ord', dir: 1, lang: 'all', tags: {} };
      apply();
    }
  });

  apply();
})();
