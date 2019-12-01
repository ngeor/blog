# blog

My blog

## Developing

Requirements:

- ruby
- jekyll

Commands:

- Start with `bundle exec jekyll serve`
- Start incremental with `bundle exec jekyll serve --incremental`
- Upgrade with `bundle update github-pages`
- Profile with `bundle exec jekyll build --profile`

## Categories and Tags

The custom script `preprocessor.py` generates pages for categories and tags.

Posts need to specify categories and tags in this way:

- for categories: specify the url segment of the category (e.g. `programming`
  instead of `Programming`)
- for tags: specify the human-friendly tag name (e.g. `.net` instead of
  `dot-net`)
