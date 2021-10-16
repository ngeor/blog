---
layout: tag
permalink: /archives/tag/resxtranslator/
title: Posts tagged with ResxTranslator
tag: ResxTranslator
post_count: 1
sort_index: 998-resxtranslator
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
