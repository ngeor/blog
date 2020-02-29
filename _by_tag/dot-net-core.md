---
layout: default
permalink: /archives/tag/dot-net-core/
title: .NET Core
post_count: 3
sort_index: 996-.net core
---
<h1 class="page-heading">Posts tagged with .NET Core</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
