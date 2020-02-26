---
layout: default
permalink: /archives/tag/aws-lambda/
title: aws lambda
post_count: 2
sort_index: 00588-aws lambda
---
<h1 class="page-heading">Posts tagged with aws lambda</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
