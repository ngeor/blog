---
layout: page
title: Series
---
I've written a few series of blog posts on topics that are too big to fit in a
single post. In this page you can find a list of all these series.

<ul class="series-list">
{%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
{%- assign posts = site.series | reverse -%}
{%- for post in posts -%}
  {%- unless post.title == 'Series' %}
  <li class="series-item">
    {%- if post.logo == 'helm' -%}
    <img class="tube" src="{{ site.baseurl }}/assets/helm-blue-vector.svg" alt="Helm">
    {%- else -%}
    <img class="tube" src="{{ site.baseurl }}/assets/test-tube-4-128.png" alt="Test tube">
    {%- endif -%}
    <section>
      <header>
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        <time class="dt-published" datetime="{{ post.date | date_to_xmlschema }}">
          {{ post.date | date: date_format }}
        </time>
      </header>
      {{ post.excerpt }}
    </section>
  </li>
  {%- endunless -%}
{%- endfor -%}
</ul>
