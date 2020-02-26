---
layout: default
permalink: /archives/tag/exiftool/
title: exiftool
post_count: 1
sort_index: 00589-exiftool
---
<h1 class="page-heading">Posts tagged with exiftool</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
