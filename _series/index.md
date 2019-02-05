---
layout: page
title: Series
---
I've written a few series of blog posts on topics that are too big to fit in a
single post. In this page you can find a list of all these series.

<ul class="series-list">
{%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
{%- assign posts = site.series | reverse -%}
{%- for series in posts -%}
  {%- unless series.title == 'Series' %}
  <li class="series-item">
    <img class="tube" src="{{ site.baseurl }}/assets/test-tube-4-128.png" alt="Test tube">
    <section>
      <header>
        <a href="{{ series.url | relative_url }}">{{ series.title }}</a>
        <time class="dt-published" datetime="{{ series.date | date_to_xmlschema }}">
          {{ series.date | date: date_format }}
        </time>
      </header>
      {{ series.excerpt }}
    </section>
  </li>
  {%- endunless -%}
{%- endfor -%}
</ul>
