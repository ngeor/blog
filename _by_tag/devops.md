---
layout: tag
permalink: /archives/tag/devops/
title: Posts tagged with devops
tag: devops
post_count: 1
sort_index: 998-devops
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
