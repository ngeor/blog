---
layout: default
permalink: /archives/tag/just-for-fun/
title: just for fun
post_count: 1
sort_index: 998-just for fun
---
<h1 class="page-heading">Posts tagged with just for fun</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
