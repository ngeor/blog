---
layout: default
permalink: /archives/tag/powershell/
title: powershell
post_count: 1
sort_index: 998-powershell
---
<h1 class="page-heading">Posts tagged with powershell</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
