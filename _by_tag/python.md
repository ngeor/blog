---
layout: tag
permalink: /archives/tag/python/
title: Posts tagged with python
tag: python
post_count: 6
sort_index: 993-python
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
