---
layout: default
permalink: /archives/tag/castle-dynamicproxy/
title: Castle DynamicProxy
post_count: 1
sort_index: 998-castle dynamicproxy
---
<h1 class="page-heading">Posts tagged with Castle DynamicProxy</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
