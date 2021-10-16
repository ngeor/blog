---
layout: tag
permalink: /archives/tag/proxyquire/
title: Posts tagged with proxyquire
tag: proxyquire
post_count: 1
sort_index: 998-proxyquire
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
