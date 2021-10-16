---
layout: tag
permalink: /archives/tag/kddbot/
title: Posts tagged with kddbot
tag: kddbot
post_count: 1
sort_index: 998-kddbot
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
