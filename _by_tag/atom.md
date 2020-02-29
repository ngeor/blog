---
layout: default
permalink: /archives/tag/atom/
title: atom
post_count: 2
sort_index: 997-atom
---
<h1 class="page-heading">Posts tagged with atom</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
