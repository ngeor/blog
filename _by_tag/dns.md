---
layout: default
permalink: /archives/tag/dns/
title: dns
post_count: 2
sort_index: 997-dns
---
<h1 class="page-heading">Posts tagged with dns</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
