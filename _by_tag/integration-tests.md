---
layout: default
permalink: /archives/tag/integration-tests/
title: integration tests
post_count: 1
sort_index: 00589-integration tests
---
<h1 class="page-heading">Posts tagged with integration tests</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
