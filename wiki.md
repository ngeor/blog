---
layout: default
title: Wiki
permalink: /wiki/
---

<h1>{{ page.title }}</h1>

The Wiki section contains reference articles that will be updated (in contrast
with blog posts which are immutable) whenever I want to modify something.

<ul class="post-list">
  {%- for post in site.wiki -%}
  <li>
    <h3>
      <a href="{{ post.url | relative_url }}">
        {{ post.title | escape }}
      </a>
    </h3>
    {%- if site.show_excerpts -%}
      {{ post.excerpt }}
    {%- endif -%}
  </li>
  {%- endfor -%}
</ul>
