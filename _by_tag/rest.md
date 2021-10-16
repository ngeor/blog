---
layout: tag
permalink: /archives/tag/rest/
title: Posts tagged with rest
tag: rest
post_count: 2
sort_index: 997-rest
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
