---
layout: default
permalink: /archives/tag/sns/
title: SNS
post_count: 2
sort_index: 00588-sns
---
<h1 class="page-heading">Posts tagged with SNS</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
