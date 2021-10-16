---
layout: tag
permalink: /archives/tag/grunt/
title: Posts tagged with grunt
tag: grunt
post_count: 1
sort_index: 998-grunt
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
