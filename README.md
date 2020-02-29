# blog

My blog

## Developing

Requirements:

- ruby
- bundler

Commands:

- Install with `bundle install --path vendor/bundle`
- Start with `bundle exec jekyll serve`
- Or, start incremental with `bundle exec jekyll serve --incremental`
- Upgrade with `bundle update github-pages`
- Profile with `bundle exec jekyll build --profile`

## New Post

Scaffold a new post with `new.rb`.

## Tags

The custom script `preprocessor.rb` generates tag pages. The tags need to be
specified in the post's front-matter using the human-friendly name (e.g. `.net`
instead of `dot-net`).

## Pages

The page layout has a top-level element `article`.

The `article` will have the data attribute `data-file` which is the file path of
the page, without the `.md` extension and with all slashes replaced by hyphens.
