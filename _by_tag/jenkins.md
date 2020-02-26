---
layout: default
permalink: /archives/tag/jenkins/
title: Jenkins
post_count: 2
sort_index: 00588-jenkins
---
<h1 class="page-heading">Posts tagged with Jenkins</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
