---
layout: tag
permalink: /archives/tag/page-object-pattern/
title: Posts tagged with page object pattern
tag: page object pattern
post_count: 2
sort_index: 997-page object pattern
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
