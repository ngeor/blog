# blog

My blog

## Developing

Requirements:

- Ruby
- Jekyll

Commands:

- Install with `bundle install`
- Start serving the site with `bundle exec jekyll serve --incremental --host 0.0.0.0`
- Upgrade with `bundle update github-pages`
- Profile with `bundle exec jekyll build --profile`

## Authoring

Scaffold a new post with `new.rb`.

The custom attribute `use_mermaid` will enable [mermaid](https://mermaid-js.github.io/mermaid/#/) diagrams.

The custom attribute `extra_css` can be used to add extra styling to a page or post.
The value of that attribute will be added to the `<body>` `class`.

### Pages

To show a page in the burger menu, tag it with `menu`.

## Tags

The custom script `preprocessor.rb` generates tag pages. The tags need to be
specified in the post's front-matter using the human-friendly name (e.g. `.net`
instead of `dot-net`).
