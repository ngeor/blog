---
layout: default
permalink: /archives/tag/tech/
title: tech
post_count: 5
sort_index: 994-tech
---
<h1 class="page-heading">Posts tagged with tech</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
