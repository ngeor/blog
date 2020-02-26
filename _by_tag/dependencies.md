---
layout: default
permalink: /archives/tag/dependencies/
title: dependencies
post_count: 1
sort_index: 00589-dependencies
---
<h1 class="page-heading">Posts tagged with dependencies</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
