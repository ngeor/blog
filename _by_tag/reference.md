---
layout: default
permalink: /archives/tag/reference/
title: reference
post_count: 7
sort_index: 992-reference
---
<h1 class="page-heading">Posts tagged with reference</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
