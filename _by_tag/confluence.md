---
layout: default
permalink: /archives/tag/confluence/
title: confluence
post_count: 2
sort_index: 997-confluence
---
<h1 class="page-heading">Posts tagged with confluence</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
