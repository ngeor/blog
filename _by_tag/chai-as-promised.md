---
layout: default
permalink: /archives/tag/chai-as-promised/
title: chai-as-promised
post_count: 2
sort_index: 00588-chai-as-promised
---
<h1 class="page-heading">Posts tagged with chai-as-promised</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
