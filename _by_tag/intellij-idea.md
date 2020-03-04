---
layout: default
permalink: /archives/tag/intellij-idea/
title: IntelliJ IDEA
post_count: 6
sort_index: 993-intellij idea
---
<h1 class="page-heading">Posts tagged with IntelliJ IDEA</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
