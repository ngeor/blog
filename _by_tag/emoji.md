---
layout: tag
permalink: /archives/tag/emoji/
title: Posts tagged with emoji
tag: emoji
post_count: 1
sort_index: 998-emoji
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
