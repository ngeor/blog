---
layout: default
permalink: /archives/tag/monorepo/
title: monorepo
post_count: 3
sort_index: 996-monorepo
---
<h1 class="page-heading">Posts tagged with monorepo</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
