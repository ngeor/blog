---
layout: default
permalink: /archives/tag/zfs/
title: zfs
post_count: 1
sort_index: 998-zfs
---
<h1 class="page-heading">Posts tagged with zfs</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
