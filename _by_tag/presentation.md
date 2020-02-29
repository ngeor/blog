---
layout: default
permalink: /archives/tag/presentation/
title: presentation
post_count: 1
sort_index: 998-presentation
---
<h1 class="page-heading">Posts tagged with presentation</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
