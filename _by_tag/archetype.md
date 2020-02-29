---
layout: default
permalink: /archives/tag/archetype/
title: archetype
post_count: 2
sort_index: 997-archetype
---
<h1 class="page-heading">Posts tagged with archetype</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
