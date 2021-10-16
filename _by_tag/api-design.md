---
layout: tag
permalink: /archives/tag/api-design/
title: Posts tagged with api design
tag: api design
post_count: 1
sort_index: 998-api design
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
