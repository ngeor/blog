---
layout: default
permalink: /archives/tag/rest/
title: rest
post_count: 1
sort_index: 00589-rest
---
<h1 class="page-heading">Posts tagged with rest</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
