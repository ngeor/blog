---
layout: tag
permalink: /archives/tag/c-sharp/
title: Posts tagged with C#
tag: C#
post_count: 20
sort_index: 979-c#
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
