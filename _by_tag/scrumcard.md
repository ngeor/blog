---
layout: tag
permalink: /archives/tag/scrumcard/
title: Posts tagged with ScrumCard
tag: ScrumCard
post_count: 1
sort_index: 998-scrumcard
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
