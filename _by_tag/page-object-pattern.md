---
layout: default
permalink: /archives/tag/page-object-pattern/
title: page object pattern
post_count: 2
sort_index: 00588-page object pattern
---
<h1 class="page-heading">Posts tagged with page object pattern</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
