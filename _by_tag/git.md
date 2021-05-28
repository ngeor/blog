---
layout: default
permalink: /archives/tag/git/
title: git
post_count: 12
sort_index: 987-git
---
<h1 class="page-heading">Posts tagged with git</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
