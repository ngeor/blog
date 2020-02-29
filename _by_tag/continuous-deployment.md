---
layout: default
permalink: /archives/tag/continuous-deployment/
title: continuous deployment
post_count: 7
sort_index: 992-continuous deployment
---
<h1 class="page-heading">Posts tagged with continuous deployment</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
