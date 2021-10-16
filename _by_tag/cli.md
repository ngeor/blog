---
layout: tag
permalink: /archives/tag/cli/
title: Posts tagged with cli
tag: cli
post_count: 1
sort_index: 998-cli
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
