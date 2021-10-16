---
layout: tag
permalink: /archives/tag/azure/
title: Posts tagged with azure
tag: azure
post_count: 2
sort_index: 997-azure
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
