---
layout: default
permalink: /archives/tag/resxtranslator/
title: ResxTranslator
post_count: 1
sort_index: 998-resxtranslator
---
<h1 class="page-heading">Posts tagged with ResxTranslator</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
