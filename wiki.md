---
layout: page
title: Wiki
permalink: /wiki/
---
The Wiki section contains reference articles that will be updated (in contrast
with blog posts which are immutable) whenever I want to modify something.

{%- for wiki in site.wiki %}

  <h2><a href="{{ wiki.url | relative_url }}">{{ wiki.title }}</a></h2>

  {{ wiki.excerpt }}

{%- endfor -%}
