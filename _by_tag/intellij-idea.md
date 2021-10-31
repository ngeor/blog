---
layout: tag
permalink: /archives/tag/intellij-idea/
title: Posts tagged with IntelliJ IDEA
tag: IntelliJ IDEA
post_count: 5
sort_index: 994-intellij idea
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
