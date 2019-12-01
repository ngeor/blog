---
layout: page
title: Archive by tag
hidden: true
---

Tags

{% assign tags = site.tag | sort: "post_count" | reverse %}

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
