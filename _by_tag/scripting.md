---
layout: tag
permalink: /archives/tag/scripting/
title: Posts tagged with scripting
tag: scripting
post_count: 1
sort_index: 998-scripting
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
