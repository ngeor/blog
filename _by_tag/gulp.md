---
layout: default
permalink: /archives/tag/gulp/
title: gulp
post_count: 1
sort_index: 00589-gulp
---
<h1 class="page-heading">Posts tagged with gulp</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
