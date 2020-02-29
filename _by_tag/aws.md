---
layout: default
permalink: /archives/tag/aws/
title: aws
post_count: 6
sort_index: 993-aws
---
<h1 class="page-heading">Posts tagged with aws</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
