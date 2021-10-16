---
layout: tag
permalink: /archives/tag/powershell/
title: Posts tagged with powershell
tag: powershell
post_count: 1
sort_index: 998-powershell
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
