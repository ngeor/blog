---
layout: tag
permalink: /archives/tag/functional-tests/
title: Posts tagged with functional tests
tag: functional tests
post_count: 12
sort_index: 987-functional tests
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
