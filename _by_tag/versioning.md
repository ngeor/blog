---
layout: default
permalink: /archives/tag/versioning/
title: versioning
post_count: 5
sort_index: 994-versioning
---
<h1 class="page-heading">Posts tagged with versioning</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
