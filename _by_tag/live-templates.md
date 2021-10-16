---
layout: tag
permalink: /archives/tag/live-templates/
title: Posts tagged with live templates
tag: live templates
post_count: 1
sort_index: 998-live templates
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
