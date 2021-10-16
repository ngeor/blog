---
layout: tag
permalink: /archives/tag/technical-debt/
title: Posts tagged with technical debt
tag: technical debt
post_count: 2
sort_index: 997-technical debt
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
