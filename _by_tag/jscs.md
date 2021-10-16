---
layout: tag
permalink: /archives/tag/jscs/
title: Posts tagged with jscs
tag: jscs
post_count: 2
sort_index: 997-jscs
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
