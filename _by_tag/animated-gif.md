---
layout: tag
permalink: /archives/tag/animated-gif/
title: Posts tagged with animated gif
tag: animated gif
post_count: 1
sort_index: 998-animated gif
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
