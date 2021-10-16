---
layout: tag
permalink: /archives/tag/code-review/
title: Posts tagged with code review
tag: code review
post_count: 4
sort_index: 995-code review
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
