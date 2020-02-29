---
layout: default
permalink: /archives/tag/ubuntu/
title: ubuntu
post_count: 5
sort_index: 994-ubuntu
---
<h1 class="page-heading">Posts tagged with ubuntu</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
