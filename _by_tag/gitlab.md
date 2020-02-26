---
layout: default
permalink: /archives/tag/gitlab/
title: GitLab
post_count: 1
sort_index: 00589-gitlab
---
<h1 class="page-heading">Posts tagged with GitLab</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
