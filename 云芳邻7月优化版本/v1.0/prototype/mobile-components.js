(function () {
  'use strict';

  function rootOf(element) {
    return element.closest('.yfl-c-root') || document.body;
  }

  function showToast(root, text) {
    var toast = root.querySelector('.m-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'm-toast';
      root.appendChild(toast);
    }
    toast.textContent = text || '操作完成';
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(function () { toast.classList.remove('show'); }, 1500);
  }

  document.addEventListener('click', function (event) {
    var target = event.target.closest('[data-m-action]');
    if (!target) return;

    var root = rootOf(target);
    var action = target.dataset.mAction;

    if (action === 'tab') {
      var group = target.closest('[data-m-group]') || target.parentElement;
      group.querySelectorAll('[data-m-action="tab"]').forEach(function (item) {
        item.classList.toggle('active', item === target);
      });
      return;
    }

    if (action === 'toggle') {
      if (!target.classList.contains('disabled')) target.classList.toggle('on');
      return;
    }

    if (action === 'select') {
      target.classList.toggle('active');
      return;
    }

    if (action === 'open-sheet' || action === 'open-dialog') {
      var selector = target.dataset.target;
      var overlay = selector ? root.querySelector(selector) : null;
      if (overlay) overlay.classList.add('show');
      return;
    }

    if (action === 'close-layer') {
      var layer = target.closest('.m-sheet-overlay,.m-dialog-overlay');
      if (layer) layer.classList.remove('show');
      return;
    }

    if (action === 'upload') {
      target.classList.toggle('filled');
      target.innerHTML = target.classList.contains('filled')
        ? '已上传<span class="m-upload-remove">×</span>'
        : '<span>+</span>';
      return;
    }

    if (action === 'toast') showToast(root, target.dataset.message);
  });

  window.YunFangLinC = { showToast: showToast };
})();
