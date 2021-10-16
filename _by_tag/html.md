---
layout: tag
permalink: /archives/tag/html/
title: Posts tagged with html
tag: html
post_count: 2
sort_index: 997-html
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
