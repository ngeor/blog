---
layout: default
permalink: /archives/tag/left-pad/
title: left-pad
post_count: 1
sort_index: 00589-left-pad
---
<h1 class="page-heading">Posts tagged with left-pad</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
