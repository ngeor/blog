---
layout: tag
permalink: /archives/tag/api/
title: Posts tagged with api
tag: api
post_count: 1
sort_index: 998-api
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
