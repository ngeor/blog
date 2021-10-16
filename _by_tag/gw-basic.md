---
layout: tag
permalink: /archives/tag/gw-basic/
title: Posts tagged with GW-Basic
tag: GW-Basic
post_count: 1
sort_index: 998-gw-basic
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
