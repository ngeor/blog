---
layout: default
permalink: /archives/tag/java/
title: java
post_count: 30
sort_index: 969-java
---
<h1 class="page-heading">Posts tagged with java</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
