---
layout: tag
permalink: /archives/tag/aws-lambda/
title: Posts tagged with aws lambda
tag: aws lambda
post_count: 2
sort_index: 997-aws lambda
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
