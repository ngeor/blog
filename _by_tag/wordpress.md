---
layout: default
permalink: /archives/tag/wordpress/
title: wordpress
post_count: 3
sort_index: 00587-wordpress
---
<h1 class="page-heading">Posts tagged with wordpress</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
