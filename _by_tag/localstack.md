---
layout: tag
permalink: /archives/tag/localstack/
title: Posts tagged with localstack
tag: localstack
post_count: 1
sort_index: 998-localstack
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
