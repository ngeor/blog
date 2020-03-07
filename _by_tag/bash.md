---
layout: default
permalink: /archives/tag/bash/
title: bash
post_count: 11
sort_index: 988-bash
---
<h1 class="page-heading">Posts tagged with bash</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
