---
layout: page
title: Archive by tag
permalink: /archives/tag/
---

Tags

{% assign tags = site.by_tag | sort: "sort_index" %}

<ul>

{% for tag in tags %}

<li>
  <a href="{{ tag.url | relative_url }}">
    {{ tag.title | escape }} ({{ tag.post_count }}
    {% if tag.post_count > 1 -%} posts {%- else -%} post {%- endif -%})
  </a>
</li>

{% endfor %}

</ul>
