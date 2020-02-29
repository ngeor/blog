---
layout: default
permalink: /archives/tag/functional-tests/
title: functional tests
post_count: 9
sort_index: 990-functional tests
---
<h1 class="page-heading">Posts tagged with functional tests</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
