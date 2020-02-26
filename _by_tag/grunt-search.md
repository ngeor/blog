---
layout: default
permalink: /archives/tag/grunt-search/
title: grunt-search
post_count: 1
sort_index: 00589-grunt-search
---
<h1 class="page-heading">Posts tagged with grunt-search</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
