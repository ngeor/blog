---
layout: tag
permalink: /archives/tag/dockerfile/
title: Posts tagged with Dockerfile
tag: Dockerfile
post_count: 1
sort_index: 998-dockerfile
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
