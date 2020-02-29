---
layout: default
permalink: /archives/tag/automation/
title: automation
post_count: 1
sort_index: 998-automation
---
<h1 class="page-heading">Posts tagged with automation</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
