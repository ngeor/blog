---
layout: default
permalink: /archives/tag/metadata/
title: metadata
post_count: 1
sort_index: 00589-metadata
---
<h1 class="page-heading">Posts tagged with metadata</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
