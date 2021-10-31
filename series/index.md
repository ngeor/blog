---
layout: page
title: Series
tags:
  - menu
extra_css: series
---
I've written a few series of blog posts on topics that are too big to fit in a
single post. In this page you can find a list of all these series.

<ul>
{%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
{%- assign posts = site.series | reverse -%}
{%- for post in posts -%}
  {%- assign sub_posts = site.posts | where: "series", post.title | reverse -%}
  {%- assign sub_post = sub_posts.first -%}
  <li>
    {%- if post.logo == 'helm' -%}
    <img src="{{ site.baseurl }}/assets/helm-blue-vector.svg" alt="Helm">
    {%- else -%}
    <img src="{{ site.baseurl }}/assets/test-tube-4-128.png" alt="Test tube">
    {%- endif -%}
    <div>
      <div class="series-list-header">
        <a href="{{ sub_post.url | relative_url }}">{{ post.title }}</a>
        <time datetime="{{ post.date | date_to_xmlschema }}">
          {{ post.date | date: date_format }}
        </time>
      </div>
      {{ post.excerpt }}
    </div>
  </li>
{%- endfor -%}
</ul>
