---
layout: tag
permalink: /archives/tag/schema/
title: Posts tagged with schema
tag: schema
post_count: 1
sort_index: 998-schema
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
