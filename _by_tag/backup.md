---
layout: tag
permalink: /archives/tag/backup/
title: Posts tagged with backup
tag: backup
post_count: 3
sort_index: 996-backup
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
