---
layout: tag
permalink: /archives/tag/postgresql/
title: Posts tagged with PostgreSQL
tag: PostgreSQL
post_count: 1
sort_index: 998-postgresql
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
