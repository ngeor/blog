---
layout: tag
permalink: /archives/tag/dependencies/
title: Posts tagged with dependencies
tag: dependencies
post_count: 4
sort_index: 995-dependencies
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
