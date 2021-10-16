---
layout: tag
permalink: /archives/tag/pull-requests/
title: Posts tagged with pull requests
tag: pull requests
post_count: 1
sort_index: 998-pull requests
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
