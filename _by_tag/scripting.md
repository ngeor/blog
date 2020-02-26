---
layout: default
permalink: /archives/tag/scripting/
title: scripting
post_count: 1
sort_index: 00589-scripting
---
<h1 class="page-heading">Posts tagged with scripting</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
