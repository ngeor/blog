---
layout: default
permalink: /archives/tag/yaml/
title: YAML
post_count: 2
sort_index: 997-yaml
---
<h1 class="page-heading">Posts tagged with YAML</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
