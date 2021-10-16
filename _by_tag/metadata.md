---
layout: tag
permalink: /archives/tag/metadata/
title: Posts tagged with metadata
tag: metadata
post_count: 1
sort_index: 998-metadata
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
