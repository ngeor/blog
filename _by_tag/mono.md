---
layout: default
permalink: /archives/tag/mono/
title: mono
post_count: 10
sort_index: 989-mono
---
<h1 class="page-heading">Posts tagged with mono</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
