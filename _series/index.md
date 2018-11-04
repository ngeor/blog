---
layout: page
title: Series
---
I've written a few series of blog posts on topics that are too big to fit in a
single post. In this page you can find a list of all these series.

{% assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
{%- for series in site.series -%}
  {%- unless series.title == 'Series' -%}

  <h2><a href="{{ series.url | relative_url }}">{{ series.title }}</a></h2>
  {{ series.date | date: date_format }}
  {{ series.excerpt }}

  {%- endunless -%}
{%- endfor -%}
