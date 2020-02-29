---
layout: default
permalink: /archives/tag/ruby/
title: ruby
post_count: 6
sort_index: 993-ruby
---
<h1 class="page-heading">Posts tagged with ruby</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
