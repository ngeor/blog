---
layout: default
permalink: /archives/tag/dashboard/
title: dashboard
post_count: 2
sort_index: 00588-dashboard
---
<h1 class="page-heading">Posts tagged with dashboard</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
