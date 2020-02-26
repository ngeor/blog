---
layout: default
permalink: /archives/tag/docker/
title: docker
post_count: 30
sort_index: 00560-docker
---
<h1 class="page-heading">Posts tagged with docker</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
