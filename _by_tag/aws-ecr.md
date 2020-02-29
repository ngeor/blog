---
layout: default
permalink: /archives/tag/aws-ecr/
title: AWS ECR
post_count: 1
sort_index: 998-aws ecr
---
<h1 class="page-heading">Posts tagged with AWS ECR</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
