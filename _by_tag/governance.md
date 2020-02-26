---
layout: default
permalink: /archives/tag/governance/
title: governance
post_count: 1
sort_index: 00589-governance
---
<h1 class="page-heading">Posts tagged with governance</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
