---
layout: default
permalink: /archives/tag/grunt-filenames/
title: grunt-filenames
post_count: 2
sort_index: 00588-grunt-filenames
---
<h1 class="page-heading">Posts tagged with grunt-filenames</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
