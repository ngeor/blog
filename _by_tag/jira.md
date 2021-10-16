---
layout: tag
permalink: /archives/tag/jira/
title: Posts tagged with jira
tag: jira
post_count: 1
sort_index: 998-jira
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
