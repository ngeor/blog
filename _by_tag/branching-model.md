---
layout: default
permalink: /archives/tag/branching-model/
title: branching model
post_count: 1
sort_index: 998-branching model
---
<h1 class="page-heading">Posts tagged with branching model</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
