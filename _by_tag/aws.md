---
layout: tag
permalink: /archives/tag/aws/
title: Posts tagged with aws
tag: aws
post_count: 6
sort_index: 993-aws
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
