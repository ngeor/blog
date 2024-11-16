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
