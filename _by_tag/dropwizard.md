---
layout: default
permalink: /archives/tag/dropwizard/
title: dropwizard
post_count: 1
sort_index: 998-dropwizard
---
<h1 class="page-heading">Posts tagged with dropwizard</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
