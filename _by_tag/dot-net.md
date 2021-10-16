---
layout: tag
permalink: /archives/tag/dot-net/
title: Posts tagged with .NET
tag: .NET
post_count: 45
sort_index: 954-.net
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
