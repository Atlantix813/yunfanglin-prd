(function () {
  'use strict';

  function rootOf(element) {
    return element.closest('.yfl-pc-root') || document.body;
  }

  function showToast(root, text) {
    var toast = root.querySelector('.pc-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'pc-toast';
      root.appendChild(toast);
    }
    toast.textContent = text || '操作成功';
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(function () { toast.classList.remove('show'); }, 1500);
  }

  document.addEventListener('click', function (event) {
    var target = event.target.closest('[data-pc-action]');
    if (!target) return;

    var root = rootOf(target);
    var action = target.dataset.pcAction;

    if (action === 'tab' || action === 'menu' || action === 'tree') {
      var group = target.closest('[data-pc-group]') || target.parentElement;
      group.querySelectorAll('[data-pc-action="' + action + '"]').forEach(function (item) {
        item.classList.toggle('active', item === target);
      });
      return;
    }

    if (action === 'toggle') {
      target.classList.toggle('on');
      target.classList.toggle('off', !target.classList.contains('on'));
      var hint = target.parentElement.querySelector('.switch-hint');
      if (hint) hint.textContent = target.classList.contains('on')
        ? (target.dataset.onText || '已开启')
        : (target.dataset.offText || '已关闭');
      return;
    }

    if (action === 'open-modal') {
      var modal = root.querySelector(target.dataset.target);
      if (modal) modal.hidden = false;
      return;
    }

    if (action === 'open-drawer') {
      var drawer = root.querySelector(target.dataset.target);
      if (drawer) drawer.hidden = false;
      return;
    }

    if (action === 'close-drawer') {
      var drawerOverlay = target.closest('.pc-drawer-overlay');
      if (drawerOverlay) drawerOverlay.hidden = true;
      return;
    }

    if (action === 'radio') {
      var radioGroup = target.closest('[data-pc-group]') || target.parentElement;
      radioGroup.querySelectorAll('[data-pc-action="radio"]').forEach(function (item) {
        item.classList.toggle('checked', item === target);
      });
      return;
    }

    if (action === 'close-modal') {
      var overlay = target.closest('.overlay');
      if (overlay) overlay.hidden = true;
      return;
    }

    if (action === 'reset') {
      var form = target.closest('.filter-card');
      if (!form) return;
      form.querySelectorAll('input').forEach(function (input) { input.value = ''; });
      form.querySelectorAll('select').forEach(function (select) { select.selectedIndex = 0; });
      showToast(root, '筛选条件已重置');
      return;
    }

    if (action === 'query') {
      showToast(root, '已按当前条件查询');
      return;
    }

    if (action === 'page') {
      var pages = target.closest('.pagination');
      if (pages) pages.querySelectorAll('[data-pc-action="page"]').forEach(function (item) { item.classList.toggle('active', item === target); });
      showToast(root, '已切换到第 ' + target.textContent.trim() + ' 页');
      return;
    }

    if (action === 'upload') {
      var filled = target.classList.toggle('filled');
      target.innerHTML = filled
        ? '<span>已上传</span><span class="pc-upload-remove">×</span>'
        : '<span class="plus">+</span><span>上传文件</span>';
      showToast(root, filled ? '上传成功' : '已移除文件');
      return;
    }

    if (action === 'save') {
      var overlay = target.closest('.overlay');
      if (overlay) overlay.hidden = true;
      showToast(root, '保存成功');
      return;
    }

    if (action === 'toast') showToast(root, target.dataset.message);
  });

  window.YunFangLinPC = { showToast: showToast };
})();
