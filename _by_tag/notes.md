---
layout: tag
permalink: /archives/tag/notes/
title: Posts tagged with notes
tag: notes
post_count: 28
sort_index: 971-notes
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
