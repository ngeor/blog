---
layout: default
permalink: /archives/tag/sinon/
title: sinon
post_count: 4
sort_index: 00586-sinon
---
<h1 class="page-heading">Posts tagged with sinon</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
