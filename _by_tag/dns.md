---
layout: tag
permalink: /archives/tag/dns/
title: Posts tagged with dns
tag: dns
post_count: 2
sort_index: 997-dns
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
