---
layout: default
permalink: /archives/tag/technical-debt/
title: technical debt
post_count: 2
sort_index: 997-technical debt
---
<h1 class="page-heading">Posts tagged with technical debt</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
