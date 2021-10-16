---
layout: tag
permalink: /archives/tag/hackathon/
title: Posts tagged with hackathon
tag: hackathon
post_count: 1
sort_index: 998-hackathon
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
