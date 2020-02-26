---
layout: default
permalink: /archives/tag/duolingo/
title: DuoLingo
post_count: 1
sort_index: 00589-duolingo
---
<h1 class="page-heading">Posts tagged with DuoLingo</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
