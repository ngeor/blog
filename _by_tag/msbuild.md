---
layout: default
permalink: /archives/tag/msbuild/
title: MSBuild
post_count: 1
sort_index: 998-msbuild
---
<h1 class="page-heading">Posts tagged with MSBuild</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
