---
layout: tag
permalink: /archives/tag/running/
title: Posts tagged with running
tag: running
post_count: 4
sort_index: 995-running
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
