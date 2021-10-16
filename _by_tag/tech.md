---
layout: tag
permalink: /archives/tag/tech/
title: Posts tagged with tech
tag: tech
post_count: 5
sort_index: 994-tech
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
