---
layout: default
permalink: /archives/tag/goals/
title: goals
post_count: 1
sort_index: 00589-goals
---
<h1 class="page-heading">Posts tagged with goals</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
