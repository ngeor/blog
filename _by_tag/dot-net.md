---
layout: default
permalink: /archives/tag/dot-net/
title: .NET
post_count: 6
sort_index: 00584-.net
---
<h1 class="page-heading">Posts tagged with .NET</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
