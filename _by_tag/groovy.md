---
layout: tag
permalink: /archives/tag/groovy/
title: Posts tagged with groovy
tag: groovy
post_count: 1
sort_index: 998-groovy
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
