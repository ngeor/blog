---
layout: tag
permalink: /archives/tag/submodules/
title: Posts tagged with submodules
tag: submodules
post_count: 1
sort_index: 998-submodules
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
