---
layout: tag
permalink: /archives/tag/smoke-test/
title: Posts tagged with smoke test
tag: smoke test
post_count: 1
sort_index: 998-smoke test
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
