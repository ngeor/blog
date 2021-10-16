---
layout: tag
permalink: /archives/tag/developers/
title: Posts tagged with developers
tag: developers
post_count: 2
sort_index: 997-developers
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
