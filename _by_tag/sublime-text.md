---
layout: default
permalink: /archives/tag/sublime-text/
title: sublime text
post_count: 1
sort_index: 998-sublime text
---
<h1 class="page-heading">Posts tagged with sublime text</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
