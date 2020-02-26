---
layout: default
permalink: /archives/tag/video/
title: video
post_count: 1
sort_index: 00589-video
---
<h1 class="page-heading">Posts tagged with video</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
