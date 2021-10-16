---
layout: tag
permalink: /archives/tag/comments/
title: Posts tagged with comments
tag: comments
post_count: 1
sort_index: 998-comments
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
