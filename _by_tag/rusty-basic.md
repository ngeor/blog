---
layout: tag
permalink: /archives/tag/rusty-basic/
title: Posts tagged with rusty basic
tag: rusty basic
post_count: 2
sort_index: 997-rusty basic
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
