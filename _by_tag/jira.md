---
layout: default
permalink: /archives/tag/jira/
title: jira
post_count: 1
sort_index: 998-jira
---
<h1 class="page-heading">Posts tagged with jira</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
