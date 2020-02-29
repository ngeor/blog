---
layout: default
permalink: /archives/tag/pet-project/
title: pet project
post_count: 5
sort_index: 994-pet project
---
<h1 class="page-heading">Posts tagged with pet project</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
