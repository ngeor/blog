---
layout: tag
permalink: /archives/tag/versioning/
title: Posts tagged with versioning
tag: versioning
post_count: 5
sort_index: 994-versioning
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
