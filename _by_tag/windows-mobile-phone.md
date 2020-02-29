---
layout: default
permalink: /archives/tag/windows-mobile-phone/
title: Windows Mobile Phone
post_count: 1
sort_index: 998-windows mobile phone
---
<h1 class="page-heading">Posts tagged with Windows Mobile Phone</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
