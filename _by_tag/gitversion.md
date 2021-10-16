---
layout: tag
permalink: /archives/tag/gitversion/
title: Posts tagged with GitVersion
tag: GitVersion
post_count: 4
sort_index: 995-gitversion
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
