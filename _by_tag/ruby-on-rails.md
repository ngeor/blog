---
layout: tag
permalink: /archives/tag/ruby-on-rails/
title: Posts tagged with ruby on rails
tag: ruby on rails
post_count: 4
sort_index: 995-ruby on rails
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
