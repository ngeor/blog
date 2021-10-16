---
layout: tag
permalink: /archives/tag/exiftool/
title: Posts tagged with exiftool
tag: exiftool
post_count: 1
sort_index: 998-exiftool
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
