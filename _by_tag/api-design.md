---
layout: default
permalink: /archives/tag/api-design/
title: api design
post_count: 1
sort_index: 998-api design
---
<h1 class="page-heading">Posts tagged with api design</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
