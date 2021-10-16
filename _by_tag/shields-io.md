---
layout: tag
permalink: /archives/tag/shields-io/
title: Posts tagged with shields.io
tag: shields.io
post_count: 1
sort_index: 998-shields.io
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
