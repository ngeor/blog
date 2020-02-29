---
layout: default
permalink: /archives/tag/keyboard-shortcuts/
title: keyboard shortcuts
post_count: 1
sort_index: 998-keyboard shortcuts
---
<h1 class="page-heading">Posts tagged with keyboard shortcuts</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
