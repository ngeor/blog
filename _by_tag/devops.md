---
layout: default
permalink: /archives/tag/devops/
title: devops
post_count: 1
sort_index: 998-devops
---
<h1 class="page-heading">Posts tagged with devops</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
