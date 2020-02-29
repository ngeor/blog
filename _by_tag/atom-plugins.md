---
layout: default
permalink: /archives/tag/atom-plugins/
title: atom-plugins
post_count: 1
sort_index: 998-atom-plugins
---
<h1 class="page-heading">Posts tagged with atom-plugins</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
