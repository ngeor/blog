---
layout: tag
permalink: /archives/tag/api-gateway/
title: Posts tagged with api gateway
tag: api gateway
post_count: 1
sort_index: 998-api gateway
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
