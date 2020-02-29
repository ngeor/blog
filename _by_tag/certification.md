---
layout: default
permalink: /archives/tag/certification/
title: certification
post_count: 4
sort_index: 995-certification
---
<h1 class="page-heading">Posts tagged with certification</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
