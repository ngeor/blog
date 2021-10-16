---
layout: tag
permalink: /archives/tag/windows-live-photo-gallery/
title: Posts tagged with Windows Live Photo Gallery
tag: Windows Live Photo Gallery
post_count: 1
sort_index: 998-windows live photo gallery
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
