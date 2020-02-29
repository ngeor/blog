---
layout: default
permalink: /archives/tag/backup/
title: backup
post_count: 3
sort_index: 996-backup
---
<h1 class="page-heading">Posts tagged with backup</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
