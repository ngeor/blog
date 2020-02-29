---
layout: default
permalink: /archives/tag/fluent-nhibernate/
title: fluent nhibernate
post_count: 1
sort_index: 998-fluent nhibernate
---
<h1 class="page-heading">Posts tagged with fluent nhibernate</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
