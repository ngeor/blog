---
layout: tag
permalink: /archives/tag/kdd/
title: Posts tagged with kdd
tag: kdd
post_count: 1
sort_index: 998-kdd
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
