---
layout: default
permalink: /archives/tag/parent-pom/
title: parent pom
post_count: 1
sort_index: 998-parent pom
---
<h1 class="page-heading">Posts tagged with parent pom</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
