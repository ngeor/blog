---
layout: default
permalink: /archives/tag/funny/
title: funny
post_count: 6
sort_index: 993-funny
---
<h1 class="page-heading">Posts tagged with funny</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
