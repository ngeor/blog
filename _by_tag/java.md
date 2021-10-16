---
layout: tag
permalink: /archives/tag/java/
title: Posts tagged with java
tag: java
post_count: 30
sort_index: 969-java
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
