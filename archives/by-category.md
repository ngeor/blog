---
layout: page
title: Archive by category
hidden: true
---

Categories

<ul>

{% assign categories = site.category | sort: "post_count" | reverse %}
{%- for category in categories %}

<li>
  <a href="{{ category.url | relative_url }}">
    {{ category.title | escape }} ({{ category.post_count }}
    {% if category.post_count > 1 -%} posts {%- else -%} post {%- endif -%})
  </a>
</li>

{% endfor %}

</ul>
