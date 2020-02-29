---
layout: default
permalink: /archives/tag/cheat-sheet/
title: cheat sheet
post_count: 8
sort_index: 991-cheat sheet
---
<h1 class="page-heading">Posts tagged with cheat sheet</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
