---
layout: tag
permalink: /archives/tag/monorepo/
title: Posts tagged with monorepo
tag: monorepo
post_count: 3
sort_index: 996-monorepo
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
