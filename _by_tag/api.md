---
layout: default
permalink: /archives/tag/api/
title: api
post_count: 1
sort_index: 998-api
---
<h1 class="page-heading">Posts tagged with api</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
