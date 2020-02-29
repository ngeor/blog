---
layout: default
permalink: /archives/tag/windows/
title: Windows
post_count: 5
sort_index: 994-windows
---
<h1 class="page-heading">Posts tagged with Windows</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
