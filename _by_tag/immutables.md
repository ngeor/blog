---
layout: default
permalink: /archives/tag/immutables/
title: immutables
post_count: 1
sort_index: 998-immutables
---
<h1 class="page-heading">Posts tagged with immutables</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
