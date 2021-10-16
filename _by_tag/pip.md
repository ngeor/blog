---
layout: tag
permalink: /archives/tag/pip/
title: Posts tagged with pip
tag: pip
post_count: 1
sort_index: 998-pip
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
