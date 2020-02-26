---
layout: default
permalink: /archives/tag/api-gateway/
title: api gateway
post_count: 1
sort_index: 00589-api gateway
---
<h1 class="page-heading">Posts tagged with api gateway</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
