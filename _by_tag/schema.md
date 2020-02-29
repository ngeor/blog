---
layout: default
permalink: /archives/tag/schema/
title: schema
post_count: 1
sort_index: 998-schema
---
<h1 class="page-heading">Posts tagged with schema</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
