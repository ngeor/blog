---
layout: tag
permalink: /archives/tag/certificates/
title: Posts tagged with certificates
tag: certificates
post_count: 1
sort_index: 998-certificates
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
