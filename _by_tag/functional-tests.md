---
layout: default
permalink: /archives/tag/functional-tests/
title: functional tests
post_count: 12
sort_index: 987-functional tests
---
<h1 class="page-heading">Posts tagged with functional tests</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
