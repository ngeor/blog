---
layout: page
title: Jekyll Cheatsheet
date: 2021-10-31
---

A cheatsheet for [Jekyll](https://jekyllrb.com/).

## Links

Link to page or asset:

{% raw %}
```
{% link /some/page/link.md %}
```
{% endraw %}

Link to post:

{% raw %}
```
{% post_url 2021/2021-10-31-post-without-file-extension %}
```
{% endraw %}

## Disable Liquid

Wrap the code in `raw` ... `endraw` tags:

{% assign open_tag  = '{' | append: '%' %}
{% assign close_tag = '%' | append: '}' %}

```
{{ open_tag }} raw {{ close_tag }}
do whatever in here
{{ open_tag }} endraw {{ close_tag }}
```

Note that rendering the `raw` ... `endraw` tags themselves
is an extra challenge solved with this trick:

{% raw %}```
{% assign open_tag  = '{' | append: '%' %}
{% assign close_tag = '%' | append: '}' %}

{{ open_tag }} raw {{ close_tag }}
do whatever in here
{{ open_tag }} endraw {{ close_tag }}
```
{% endraw %}
