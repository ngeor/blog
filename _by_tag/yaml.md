---
layout: tag
permalink: /archives/tag/yaml/
title: Posts tagged with YAML
tag: YAML
post_count: 2
sort_index: 997-yaml
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
