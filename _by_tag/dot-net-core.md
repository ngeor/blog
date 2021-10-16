---
layout: tag
permalink: /archives/tag/dot-net-core/
title: Posts tagged with .NET Core
tag: .NET Core
post_count: 3
sort_index: 996-.net core
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
