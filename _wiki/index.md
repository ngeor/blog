---
layout: page
title: Wiki
---
The Wiki section contains reference articles that will be updated (in contrast
with blog posts which are immutable) whenever I want to modify something.

{% assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
{%- for wiki in site.wiki -%}
  {%- unless wiki.title == 'Wiki' -%}

  <h2><a href="{{ wiki.url | relative_url }}">{{ wiki.title }}</a></h2>
  {{ wiki.date | date: date_format }}
  {{ wiki.excerpt }}

  {%- endunless -%}
{%- endfor -%}
