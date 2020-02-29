---
layout: default
permalink: /archives/tag/ruby-on-rails/
title: ruby on rails
post_count: 4
sort_index: 995-ruby on rails
---
<h1 class="page-heading">Posts tagged with ruby on rails</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
