---
layout: tag
permalink: /archives/tag/certification/
title: Posts tagged with certification
tag: certification
post_count: 4
sort_index: 995-certification
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
