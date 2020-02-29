---
layout: default
permalink: /archives/tag/cruisecontrol/
title: CruiseControl
post_count: 1
sort_index: 998-cruisecontrol
---
<h1 class="page-heading">Posts tagged with CruiseControl</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
