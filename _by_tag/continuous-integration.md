---
layout: default
permalink: /archives/tag/continuous-integration/
title: continuous integration
post_count: 19
sort_index: 980-continuous integration
---
<h1 class="page-heading">Posts tagged with continuous integration</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
