---
layout: tag
permalink: /archives/tag/promises/
title: Posts tagged with promises
tag: promises
post_count: 2
sort_index: 997-promises
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
