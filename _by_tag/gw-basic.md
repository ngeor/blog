---
layout: default
permalink: /archives/tag/gw-basic/
title: GW-Basic
post_count: 1
sort_index: 998-gw-basic
---
<h1 class="page-heading">Posts tagged with GW-Basic</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
