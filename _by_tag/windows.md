---
layout: tag
permalink: /archives/tag/windows/
title: Posts tagged with Windows
tag: Windows
post_count: 6
sort_index: 993-windows
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
