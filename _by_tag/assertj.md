---
layout: default
permalink: /archives/tag/assertj/
title: AssertJ
post_count: 1
sort_index: 998-assertj
---
<h1 class="page-heading">Posts tagged with AssertJ</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
