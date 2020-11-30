---
layout: default
permalink: /archives/tag/rusty-basic/
title: rusty basic
post_count: 2
sort_index: 997-rusty basic
---
<h1 class="page-heading">Posts tagged with rusty basic</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
