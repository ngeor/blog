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

## Categories and Tags

The custom script `preprocessor.rb` generates pages for categories and tags.

Posts need to specify categories and tags in this way:

- for categories: specify the url segment of the category (e.g. `programming`
  instead of `Programming`)
- for tags: specify the human-friendly tag name (e.g. `.net` instead of
  `dot-net`)

## Pages

The page layout has a top-level element `article`.

The `article` will have the data attribute `data-file` which is the file path of
the page, without the `.md` extension and with all slashes replaced by hyphens.
