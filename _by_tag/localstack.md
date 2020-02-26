---
layout: default
permalink: /archives/tag/localstack/
title: localstack
post_count: 1
sort_index: 00589-localstack
---
<h1 class="page-heading">Posts tagged with localstack</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
