(function () {
  /**
   * Adds an event listener.
   * Copied from http://youmightnotneedjquery.com/
   */
  function addEventListener(el, eventName, handler) {
    if (el.addEventListener) {
      el.addEventListener(eventName, handler);
    } else {
      el.attachEvent('on' + eventName, function () {
        handler.call(el);
      });
    }
  }

  /**
   * js module for /fibonacci
   */
  const fibonacciModule = {
    /**
     * Module will only run if an element can be found using this selector.
     */
    selector: 'article[data-file="fibonacci"]',

    hideAllCodeBlocks: function () {
      document.querySelectorAll('div.code').forEach((el) => {
        el.classList.add('hide');
      });
    },

    /**
     * Main method of the module.
     */
    main: function () {
      const that = this;
      this.hideAllCodeBlocks();

      document.querySelectorAll('a.selector').forEach((el) => {
        addEventListener(el, 'click', function (e) {
          e.preventDefault();
          that.hideAllCodeBlocks();
          document.getElementById(e.currentTarget.getAttribute('data-rel')).classList.remove('hide');
        });
      });
    }
  };

  const cookiesModule = {
    // so that it runs on every page
    selector: 'body',

    /**
     * Checks if the user has acknowledged the usage of cookies.
     */
    hasAcknowledgedCookies: function () {
      // https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie#Example_3_Do_something_only_once
      return document.cookie.replace(/(?:(?:^|.*;\s*)ackCookies\s*\=\s*([^;]*).*$)|^.*$/, "$1") === "true";
    },

    /**
   * Stores a cookie to indicate that the user has acknowledged the usage of cookies.
   */
    acknowledgedCookies: function () {
      document.cookie = "ackCookies=true; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/";
    },

    showCookiesPopup: function () {
      if (this.hasAcknowledgedCookies()) {
        return;
      }

      const that = this;
      var el = document.getElementById('js-cookies');

      // show the cookie popup
      el.className = 'cookies';
      addEventListener(document.getElementById('js-cookies-close'), 'click', function (event) {
        event.preventDefault();

        // hide the cookie popup
        el.className = 'cookies cookies--acknowledged';

        // store a cookie to not show the popup next time
        that.acknowledgedCookies();
      });
    },

    main: function() {
      this.showCookiesPopup();
    }
  };

  function main() {
    const modules = [
      cookiesModule,
      fibonacciModule
    ];

    for (let i = 0; i < modules.length; i++) {
      const module = modules[i];
      if (document.querySelector(module.selector)) {
        module.main();
      }
    }
  }

  /**
   * Runs the given function when the document is ready.
   * Copied from http://youmightnotneedjquery.com/
   */
  function ready(fn) {
    if (document.readyState != 'loading') {
      fn();
    } else if (document.addEventListener) {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      document.attachEvent('onreadystatechange', function () {
        if (document.readyState != 'loading')
          fn();
      });
    }
  }

  ready(main);
})();
