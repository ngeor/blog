---
layout: default
permalink: /archives/tag/code-review/
title: code review
post_count: 4
sort_index: 00586-code review
---
<h1 class="page-heading">Posts tagged with code review</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
