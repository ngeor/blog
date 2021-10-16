---
layout: tag
permalink: /archives/tag/chai-as-promised/
title: Posts tagged with chai-as-promised
tag: chai-as-promised
post_count: 2
sort_index: 997-chai-as-promised
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
