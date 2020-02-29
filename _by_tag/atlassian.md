---
layout: default
permalink: /archives/tag/atlassian/
title: atlassian
post_count: 4
sort_index: 995-atlassian
---
<h1 class="page-heading">Posts tagged with atlassian</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
