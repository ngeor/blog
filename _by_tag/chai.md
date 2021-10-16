---
layout: tag
permalink: /archives/tag/chai/
title: Posts tagged with chai
tag: chai
post_count: 6
sort_index: 993-chai
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
