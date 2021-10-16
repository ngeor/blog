---
layout: tag
permalink: /archives/tag/ruby/
title: Posts tagged with ruby
tag: ruby
post_count: 6
sort_index: 993-ruby
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
