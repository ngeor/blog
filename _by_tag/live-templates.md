---
layout: default
permalink: /archives/tag/live-templates/
title: live templates
post_count: 1
sort_index: 998-live templates
---
<h1 class="page-heading">Posts tagged with live templates</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
