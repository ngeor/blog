---
layout: tag
permalink: /archives/tag/jacoco/
title: Posts tagged with jacoco
tag: jacoco
post_count: 3
sort_index: 996-jacoco
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
