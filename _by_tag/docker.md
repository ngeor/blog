---
layout: tag
permalink: /archives/tag/docker/
title: Posts tagged with docker
tag: docker
post_count: 30
sort_index: 969-docker
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
