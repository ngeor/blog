---
layout: page
title: Pages
tags:
  - menu
---

{% assign my_pages = site.pages | sort: "title" %}
{% for my_page in my_pages %}
    {% if my_page.title and my_page.published != false %}
        {% assign url_parts = my_page.url | split: "/" %}
        {% if url_parts.size == 3 and url_parts[1] == "pages" %}
- [{{my_page.title | escape}}]({{ my_page.url | relative_url }})
        {% endif %}
    {% endif %}
{% endfor %}
