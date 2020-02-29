---
layout: default
permalink: /archives/tag/animated-gif/
title: animated gif
post_count: 1
sort_index: 998-animated gif
---
<h1 class="page-heading">Posts tagged with animated gif</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
