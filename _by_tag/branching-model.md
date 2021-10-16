---
layout: tag
permalink: /archives/tag/branching-model/
title: Posts tagged with branching model
tag: branching model
post_count: 1
sort_index: 998-branching model
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
