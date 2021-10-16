---
layout: tag
permalink: /archives/tag/git/
title: Posts tagged with git
tag: git
post_count: 12
sort_index: 987-git
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
