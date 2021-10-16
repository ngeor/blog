---
layout: tag
permalink: /archives/tag/cruisecontrol/
title: Posts tagged with CruiseControl
tag: CruiseControl
post_count: 1
sort_index: 998-cruisecontrol
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
