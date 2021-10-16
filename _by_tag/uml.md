---
layout: tag
permalink: /archives/tag/uml/
title: Posts tagged with uml
tag: uml
post_count: 1
sort_index: 998-uml
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
