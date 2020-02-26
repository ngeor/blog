---
layout: default
permalink: /archives/tag/emoji/
title: emoji
post_count: 1
sort_index: 00589-emoji
---
<h1 class="page-heading">Posts tagged with emoji</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
