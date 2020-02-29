---
layout: default
permalink: /archives/tag/developers/
title: developers
post_count: 2
sort_index: 997-developers
---
<h1 class="page-heading">Posts tagged with developers</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
