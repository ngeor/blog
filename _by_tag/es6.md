---
layout: tag
permalink: /archives/tag/es6/
title: Posts tagged with es6
tag: es6
post_count: 1
sort_index: 998-es6
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
