---
layout: default
permalink: /archives/tag/kafka/
title: kafka
post_count: 5
sort_index: 994-kafka
---
<h1 class="page-heading">Posts tagged with kafka</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
