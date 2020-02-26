---
layout: default
permalink: /archives/tag/microservices/
title: microservices
post_count: 5
sort_index: 00585-microservices
---
<h1 class="page-heading">Posts tagged with microservices</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
