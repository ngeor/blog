---
layout: default
permalink: /archives/tag/grunt/
title: grunt
post_count: 1
sort_index: 998-grunt
---
<h1 class="page-heading">Posts tagged with grunt</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
