---
layout: default
permalink: /archives/tag/notes/
title: notes
post_count: 11
sort_index: 988-notes
---
<h1 class="page-heading">Posts tagged with notes</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
