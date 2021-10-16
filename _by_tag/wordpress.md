---
layout: tag
permalink: /archives/tag/wordpress/
title: Posts tagged with wordpress
tag: wordpress
post_count: 4
sort_index: 995-wordpress
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
