---
layout: default
permalink: /archives/tag/python/
title: python
post_count: 6
sort_index: 993-python
---
<h1 class="page-heading">Posts tagged with python</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
