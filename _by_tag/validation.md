---
layout: tag
permalink: /archives/tag/validation/
title: Posts tagged with validation
tag: validation
post_count: 2
sort_index: 997-validation
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
