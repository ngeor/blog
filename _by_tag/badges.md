---
layout: default
permalink: /archives/tag/badges/
title: badges
post_count: 2
sort_index: 00588-badges
---
<h1 class="page-heading">Posts tagged with badges</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
