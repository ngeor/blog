---
layout: page
title: Series
---
I've written a few series of blog posts on topics that are too big to fit in a
single post. In this page you can find a list of all these series.

<div class="series-list">
{%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
{%- assign posts = site.series | reverse -%}
{%- for series in posts -%}
  {%- unless series.title == 'Series' %}
  <div class="series-item">
    <div class="series-item-header">
      <h2><a href="{{ series.url | relative_url }}">{{ series.title }}</a></h2>
      <p class="post-meta">
        <time class="dt-published" datetime="{{ series.date | date_to_xmlschema }}">
          {{ series.date | date: date_format }}
        </time>
      </p>
    </div>
    <div class="series-item-body">
      <div>
        {{ series.excerpt }}
      </div>
      <a href="{{ series.url | relative_url }}"><i class="fas fa-arrow-circle-right"></i></a>
    </div>
  </div>
  {%- endunless -%}
{%- endfor -%}
</div>
