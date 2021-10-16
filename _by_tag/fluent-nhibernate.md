---
layout: tag
permalink: /archives/tag/fluent-nhibernate/
title: Posts tagged with fluent nhibernate
tag: fluent nhibernate
post_count: 1
sort_index: 998-fluent nhibernate
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
