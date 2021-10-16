---
layout: tag
permalink: /archives/tag/continuous-deployment/
title: Posts tagged with continuous deployment
tag: continuous deployment
post_count: 7
sort_index: 992-continuous deployment
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
