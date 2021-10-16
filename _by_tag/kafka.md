---
layout: tag
permalink: /archives/tag/kafka/
title: Posts tagged with kafka
tag: kafka
post_count: 5
sort_index: 994-kafka
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
