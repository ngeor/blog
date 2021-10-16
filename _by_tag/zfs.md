---
layout: tag
permalink: /archives/tag/zfs/
title: Posts tagged with zfs
tag: zfs
post_count: 1
sort_index: 998-zfs
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
