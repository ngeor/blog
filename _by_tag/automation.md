---
layout: tag
permalink: /archives/tag/automation/
title: Posts tagged with automation
tag: automation
post_count: 1
sort_index: 998-automation
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
