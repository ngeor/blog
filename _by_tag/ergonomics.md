---
layout: tag
permalink: /archives/tag/ergonomics/
title: Posts tagged with ergonomics
tag: ergonomics
post_count: 1
sort_index: 998-ergonomics
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
