---
layout: tag
permalink: /archives/tag/static-code-analysis/
title: Posts tagged with static code analysis
tag: static code analysis
post_count: 6
sort_index: 993-static code analysis
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
