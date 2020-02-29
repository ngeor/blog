---
layout: default
permalink: /archives/tag/gitversion/
title: GitVersion
post_count: 4
sort_index: 995-gitversion
---
<h1 class="page-heading">Posts tagged with GitVersion</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
