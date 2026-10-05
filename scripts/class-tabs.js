(function () {
  var root = document.querySelector('[data-tabs]');
  if (!root) return;

  var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
  var panels = Array.prototype.slice.call(root.querySelectorAll('[role="tabpanel"]'));
  var validIds = tabs.map(function (tab) { return tab.getAttribute('data-tab'); });

  function activate(id, updateHash) {
    if (validIds.indexOf(id) === -1) id = 'days';

    tabs.forEach(function (tab) {
      var selected = tab.getAttribute('data-tab') === id;
      tab.setAttribute('aria-selected', selected ? 'true' : 'false');
      tab.tabIndex = selected ? 0 : -1;
    });

    panels.forEach(function (panel) {
      var match = panel.getAttribute('data-panel') === id;
      if (match) {
        panel.removeAttribute('hidden');
      } else {
        panel.setAttribute('hidden', '');
      }
    });

    if (updateHash) {
      if (id === 'days') {
        history.replaceState(null, '', window.location.pathname + window.location.search);
      } else {
        history.replaceState(null, '', '#' + id);
      }
    }
  }

  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      activate(tab.getAttribute('data-tab'), true);
    });

    tab.addEventListener('keydown', function (event) {
      var index = tabs.indexOf(tab);
      var next = index;

      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
        next = (index + 1) % tabs.length;
      } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
        next = (index - 1 + tabs.length) % tabs.length;
      } else if (event.key === 'Home') {
        next = 0;
      } else if (event.key === 'End') {
        next = tabs.length - 1;
      } else {
        return;
      }

      event.preventDefault();
      tabs[next].focus();
      activate(tabs[next].getAttribute('data-tab'), true);
    });
  });

  var hash = (window.location.hash || '').replace(/^#/, '');
  activate(hash || 'days', false);

  window.addEventListener('hashchange', function () {
    activate((window.location.hash || '').replace(/^#/, '') || 'days', false);
  });
})();
