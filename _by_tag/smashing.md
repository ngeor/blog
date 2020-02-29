---
layout: default
permalink: /archives/tag/smashing/
title: smashing
post_count: 2
sort_index: 997-smashing
---
<h1 class="page-heading">Posts tagged with smashing</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
