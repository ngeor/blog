---
layout: default
permalink: /archives/tag/kubernetes/
title: kubernetes
post_count: 12
sort_index: 00578-kubernetes
---
<h1 class="page-heading">Posts tagged with kubernetes</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
