---
layout: default
permalink: /archives/tag/windows-live-photo-gallery/
title: Windows Live Photo Gallery
post_count: 1
sort_index: 998-windows live photo gallery
---
<h1 class="page-heading">Posts tagged with Windows Live Photo Gallery</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
