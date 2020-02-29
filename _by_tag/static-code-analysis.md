---
layout: default
permalink: /archives/tag/static-code-analysis/
title: static code analysis
post_count: 6
sort_index: 993-static code analysis
---
<h1 class="page-heading">Posts tagged with static code analysis</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
