---
layout: default
permalink: /archives/tag/diagrams/
title: diagrams
post_count: 1
sort_index: 998-diagrams
---
<h1 class="page-heading">Posts tagged with diagrams</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
