---
layout: default
permalink: /archives/tag/personal/
title: personal
post_count: 19
sort_index: 980-personal
---
<h1 class="page-heading">Posts tagged with personal</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
