---
layout: tag
permalink: /archives/tag/integration-tests/
title: Posts tagged with integration tests
tag: integration tests
post_count: 1
sort_index: 998-integration tests
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
