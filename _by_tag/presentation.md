---
layout: tag
permalink: /archives/tag/presentation/
title: Posts tagged with presentation
tag: presentation
post_count: 1
sort_index: 998-presentation
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
