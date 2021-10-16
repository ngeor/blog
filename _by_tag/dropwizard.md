---
layout: tag
permalink: /archives/tag/dropwizard/
title: Posts tagged with dropwizard
tag: dropwizard
post_count: 1
sort_index: 998-dropwizard
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
