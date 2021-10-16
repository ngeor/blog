---
layout: tag
permalink: /archives/tag/msbuild/
title: Posts tagged with msbuild
tag: msbuild
post_count: 3
sort_index: 996-msbuild
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
