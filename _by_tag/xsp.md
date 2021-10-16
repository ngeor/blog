---
layout: tag
permalink: /archives/tag/xsp/
title: Posts tagged with xsp
tag: xsp
post_count: 1
sort_index: 998-xsp
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
