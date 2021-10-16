---
layout: tag
permalink: /archives/tag/nested-classes/
title: Posts tagged with nested classes
tag: nested classes
post_count: 1
sort_index: 998-nested classes
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
