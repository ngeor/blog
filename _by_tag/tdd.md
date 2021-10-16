---
layout: tag
permalink: /archives/tag/tdd/
title: Posts tagged with tdd
tag: tdd
post_count: 2
sort_index: 997-tdd
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
