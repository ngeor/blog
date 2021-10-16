---
layout: tag
permalink: /archives/tag/gitlab/
title: Posts tagged with GitLab
tag: GitLab
post_count: 1
sort_index: 998-gitlab
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
