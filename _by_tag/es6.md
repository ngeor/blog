---
layout: default
permalink: /archives/tag/es6/
title: es6
post_count: 1
sort_index: 00589-es6
---
<h1 class="page-heading">Posts tagged with es6</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
