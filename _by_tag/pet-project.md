---
layout: tag
permalink: /archives/tag/pet-project/
title: Posts tagged with pet project
tag: pet project
post_count: 23
sort_index: 976-pet project
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
