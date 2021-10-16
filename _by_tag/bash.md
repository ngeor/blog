---
layout: tag
permalink: /archives/tag/bash/
title: Posts tagged with bash
tag: bash
post_count: 11
sort_index: 988-bash
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
