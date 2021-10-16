---
layout: tag
permalink: /archives/tag/assertj/
title: Posts tagged with AssertJ
tag: AssertJ
post_count: 1
sort_index: 998-assertj
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
