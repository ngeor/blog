---
layout: tag
permalink: /archives/tag/grunt-filenames/
title: Posts tagged with grunt-filenames
tag: grunt-filenames
post_count: 2
sort_index: 997-grunt-filenames
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
