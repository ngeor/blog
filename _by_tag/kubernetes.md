---
layout: tag
permalink: /archives/tag/kubernetes/
title: Posts tagged with kubernetes
tag: kubernetes
post_count: 12
sort_index: 987-kubernetes
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
