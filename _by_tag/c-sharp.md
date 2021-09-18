---
layout: default
permalink: /archives/tag/c-sharp/
title: C#
post_count: 20
sort_index: 979-c#
---
<h1 class="page-heading">Posts tagged with C#</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
