---
layout: tag
permalink: /archives/tag/duolingo/
title: Posts tagged with DuoLingo
tag: DuoLingo
post_count: 1
sort_index: 998-duolingo
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
