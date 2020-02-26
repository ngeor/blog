---
layout: default
permalink: /archives/tag/scrumcard/
title: ScrumCard
post_count: 1
sort_index: 00589-scrumcard
---
<h1 class="page-heading">Posts tagged with ScrumCard</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
