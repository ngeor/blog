---
layout: default
permalink: /archives/tag/proxyquire/
title: proxyquire
post_count: 1
sort_index: 998-proxyquire
---
<h1 class="page-heading">Posts tagged with proxyquire</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
