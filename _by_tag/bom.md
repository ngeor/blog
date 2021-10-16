---
layout: tag
permalink: /archives/tag/bom/
title: Posts tagged with bom
tag: bom
post_count: 1
sort_index: 998-bom
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
