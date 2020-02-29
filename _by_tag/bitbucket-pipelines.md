---
layout: default
permalink: /archives/tag/bitbucket-pipelines/
title: bitbucket pipelines
post_count: 1
sort_index: 998-bitbucket pipelines
---
<h1 class="page-heading">Posts tagged with bitbucket pipelines</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
