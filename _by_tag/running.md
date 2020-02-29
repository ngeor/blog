---
layout: default
permalink: /archives/tag/running/
title: running
post_count: 2
sort_index: 997-running
---
<h1 class="page-heading">Posts tagged with running</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
