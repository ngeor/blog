(function () {
  function ready(fn) {
    if (document.readyState != 'loading') {
      fn();
    } else {
      document.addEventListener('DOMContentLoaded', fn);
    }
  }

  function hideAllCodeBlocks() {
    document.querySelectorAll('div.code').forEach((el) => {
      el.classList.add('hide');
    });
  }

  function main() {
    hideAllCodeBlocks();

    document.querySelectorAll('a.selector').forEach((el) => {
      el.addEventListener('click', function (e) {
        e.preventDefault();
        hideAllCodeBlocks();
        document.getElementById(e.currentTarget.getAttribute('data-rel')).classList.remove('hide');
      });
    });
  }

  ready(main);
})();
