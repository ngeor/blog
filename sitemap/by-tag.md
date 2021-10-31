---
layout: page
title: Tag cloud
permalink: /sitemap/tag-cloud/
extra_css: sitemap-by-tag
---

Find posts tagged with a specific tag.

{% assign tags = site.by_tag | sort_natural: "tag" %}

<ul>

    {%- for tag_page in tags -%}
        {%- assign font_size = tag_page.post_count | times: 500.0 | divided_by: tags.size | at_least: 10 -%}

        <li>
            <a href="{{ tag_page.url | relative_url }}" style="font-size: {{- font_size -}}px">
                {{ tag_page.tag | escape }} ({{ tag_page.post_count }}
                {% if tag_page.post_count > 1 -%} posts {%- else -%} post {%- endif -%})
            </a>
        </li>

    {%- endfor -%}

</ul>
