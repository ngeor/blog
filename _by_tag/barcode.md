---
layout: default
permalink: /archives/tag/barcode/
title: barcode
post_count: 1
sort_index: 998-barcode
---
<h1 class="page-heading">Posts tagged with barcode</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
