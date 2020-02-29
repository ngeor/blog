---
layout: default
permalink: /archives/tag/nested-classes/
title: nested classes
post_count: 1
sort_index: 998-nested classes
---
<h1 class="page-heading">Posts tagged with nested classes</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
