(function () {
  /**
   * Runs the given function when the document is ready.
   * Copied from http://youmightnotneedjquery.com/
   */
  function ready(fn) {
    if (document.readyState != 'loading'){
      fn();
    } else if (document.addEventListener) {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      document.attachEvent('onreadystatechange', function() {
        if (document.readyState != 'loading')
          fn();
      });
    }
  }

  /**
   * Adds an event listener.
   * Copied from http://youmightnotneedjquery.com/
   */
  function addEventListener(el, eventName, handler) {
    if (el.addEventListener) {
      el.addEventListener(eventName, handler);
    } else {
      el.attachEvent('on' + eventName, function(){
        handler.call(el);
      });
    }
  }

  /**
   * Checks if the user has acknowledged the usage of cookies.
   */
  function hasAcknowledgedCookies() {
    // https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie#Example_3_Do_something_only_once
    return document.cookie.replace(/(?:(?:^|.*;\s*)ackCookies\s*\=\s*([^;]*).*$)|^.*$/, "$1") === "true";
  }

  /**
   * Stores a cookie to indicate that the user has acknowledged the usage of cookies.
   */
  function acknowledgedCookies() {
    document.cookie = "ackCookies=true; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/";
  }

  function showCookiesPopup() {
    if (!hasAcknowledgedCookies()) {
      var el = document.getElementById('js-cookies');

      // show the cookie popup
      el.className = 'cookies';
      addEventListener(document.getElementById('js-cookies-close'), 'click', function (event) {
        // hide the cookie popup
        el.className = 'cookies cookies--acknowledged';

        // store a cookie to not show the popup next time
        acknowledgedCookies();

        event.preventDefault();
      });
    }
  }

  function main() {
    showCookiesPopup();
  }

  ready(main);
})();
