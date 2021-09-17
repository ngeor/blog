---
layout: page
title: Sitemap
tags:
  - menu
---

## Posts

{% assign my_posts = site.posts %}
{% assign last_year = "" %}
{% for my_post in my_posts %}
  {% assign post_year = my_post.date | date: "%Y" %}
  {% if last_year != post_year %}
    {% assign last_year = post_year %}
### {{ post_year }}
  {% endif %}  
- [{{ my_post.title | escape }}]({{ my_post.url | relative_url }})
{% endfor %}

## Pages

{% assign my_pages = site.pages | sort: "title" %}
{% for my_page in my_pages %}
  {% if my_page.title %}
    {% assign url_parts = my_page.url | split: "/" %}
    {% if url_parts.size == 2 %}
- [{{my_page.title | escape}}]({{ my_page.url | relative_url }})

{% for my_child_page in my_pages %}
{% assign child_url_parts = my_child_page.url | split: "/" %}
{% if child_url_parts.size == 3 and child_url_parts[0] == url_parts[0] and child_url_parts[1] == url_parts[1] %}
  - [{{my_child_page.title | escape}}]({{ my_child_page.url | relative_url }})

{% for my_grand_child_page in my_pages %}
{% assign grand_child_url_parts = my_grand_child_page.url | split: "/" %}
{% if grand_child_url_parts.size == 4 and grand_child_url_parts[0] == url_parts[0] and grand_child_url_parts[1] == url_parts[1] and grand_child_url_parts[2] == child_url_parts[2] %}
    - [{{my_grand_child_page.title | escape}}]({{ my_grand_child_page.url | relative_url }})
{% endif %}
{% endfor %}

{% endif %}
{% endfor %}

    {% endif %}
  {% endif %}
{% endfor %}
