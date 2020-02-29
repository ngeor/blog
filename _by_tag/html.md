---
layout: default
permalink: /archives/tag/html/
title: html
post_count: 2
sort_index: 997-html
---
<h1 class="page-heading">Posts tagged with html</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
