---
layout: default
permalink: /archives/tag/kafka/
title: kafka
post_count: 4
sort_index: 995-kafka
---
<h1 class="page-heading">Posts tagged with kafka</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
