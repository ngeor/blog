---
layout: tag
permalink: /archives/tag/yagni/
title: Posts tagged with yagni
tag: yagni
post_count: 1
sort_index: 998-yagni
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
