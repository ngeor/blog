---
layout: default
permalink: /archives/tag/continuous-delivery/
title: continuous delivery
post_count: 4
sort_index: 995-continuous delivery
---
<h1 class="page-heading">Posts tagged with continuous delivery</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
