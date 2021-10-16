---
layout: tag
permalink: /archives/tag/badges/
title: Posts tagged with badges
tag: badges
post_count: 2
sort_index: 997-badges
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
