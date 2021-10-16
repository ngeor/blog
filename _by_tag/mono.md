---
layout: tag
permalink: /archives/tag/mono/
title: Posts tagged with mono
tag: mono
post_count: 10
sort_index: 989-mono
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
