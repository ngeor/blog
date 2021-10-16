---
layout: tag
permalink: /archives/tag/aws-ecr/
title: Posts tagged with AWS ECR
tag: AWS ECR
post_count: 1
sort_index: 998-aws ecr
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
