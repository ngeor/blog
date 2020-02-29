---
layout: default
permalink: /archives/tag/automated-tests/
title: automated tests
post_count: 2
sort_index: 997-automated tests
---
<h1 class="page-heading">Posts tagged with automated tests</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
