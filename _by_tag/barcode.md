---
layout: tag
permalink: /archives/tag/barcode/
title: Posts tagged with barcode
tag: barcode
post_count: 1
sort_index: 998-barcode
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
