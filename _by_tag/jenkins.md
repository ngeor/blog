---
layout: tag
permalink: /archives/tag/jenkins/
title: Posts tagged with Jenkins
tag: Jenkins
post_count: 2
sort_index: 997-jenkins
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
