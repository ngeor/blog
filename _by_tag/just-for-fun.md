---
layout: tag
permalink: /archives/tag/just-for-fun/
title: Posts tagged with just for fun
tag: just for fun
post_count: 2
sort_index: 997-just for fun
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
