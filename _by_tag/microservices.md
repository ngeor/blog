---
layout: tag
permalink: /archives/tag/microservices/
title: Posts tagged with microservices
tag: microservices
post_count: 5
sort_index: 994-microservices
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
