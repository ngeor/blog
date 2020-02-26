---
layout: default
permalink: /archives/tag/yagni/
title: yagni
post_count: 1
sort_index: 00589-yagni
---
<h1 class="page-heading">Posts tagged with yagni</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
