---
layout: default
permalink: /archives/tag/postgresql/
title: PostgreSQL
post_count: 1
sort_index: 998-postgresql
---
<h1 class="page-heading">Posts tagged with PostgreSQL</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
