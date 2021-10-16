---
layout: tag
permalink: /archives/tag/ci-tooling/
title: Posts tagged with ci tooling
tag: ci tooling
post_count: 3
sort_index: 996-ci tooling
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
