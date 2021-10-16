---
layout: tag
permalink: /archives/tag/goals/
title: Posts tagged with goals
tag: goals
post_count: 1
sort_index: 998-goals
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
