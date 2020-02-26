---
layout: default
permalink: /archives/tag/promises/
title: promises
post_count: 2
sort_index: 00588-promises
---
<h1 class="page-heading">Posts tagged with promises</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
