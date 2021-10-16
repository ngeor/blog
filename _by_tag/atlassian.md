---
layout: tag
permalink: /archives/tag/atlassian/
title: Posts tagged with atlassian
tag: atlassian
post_count: 4
sort_index: 995-atlassian
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
