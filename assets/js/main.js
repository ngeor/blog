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

        main: function () {
            this.showCookiesPopup();
        }
    };

    const linksModule = {
        selector: 'article',
        main: function() {
            const headings = document.querySelectorAll('article h2[id]');
            for (let i = headings.length - 1; i >= 0; i--) {
                const heading = headings[i];
                const headingId = heading.getAttribute('id');
                const newLink = document.createElement('a');
                newLink.setAttribute('class', 'heading-link');
                newLink.setAttribute('href', '#' + headingId);
                newLink.appendChild(document.createTextNode("#"));
                heading.insertAdjacentElement('beforeend', newLink);
            }
        }
    };

    function main() {
        const modules = [
            cookiesModule,
            linksModule
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
