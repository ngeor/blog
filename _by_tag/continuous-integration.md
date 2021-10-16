---
layout: tag
permalink: /archives/tag/continuous-integration/
title: Posts tagged with continuous integration
tag: continuous integration
post_count: 19
sort_index: 980-continuous integration
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
