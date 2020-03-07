---
layout: default
permalink: /archives/tag/certificates/
title: certificates
post_count: 1
sort_index: 998-certificates
---
<h1 class="page-heading">Posts tagged with certificates</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
