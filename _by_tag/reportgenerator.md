---
layout: default
permalink: /archives/tag/reportgenerator/
title: ReportGenerator
post_count: 1
sort_index: 998-reportgenerator
---
<h1 class="page-heading">Posts tagged with ReportGenerator</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
