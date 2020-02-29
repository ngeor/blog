---
layout: default
permalink: /archives/tag/readability/
title: readability
post_count: 2
sort_index: 997-readability
---
<h1 class="page-heading">Posts tagged with readability</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
