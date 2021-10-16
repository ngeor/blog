---
layout: tag
permalink: /archives/tag/funny/
title: Posts tagged with funny
tag: funny
post_count: 6
sort_index: 993-funny
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
