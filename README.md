# blog

My blog

## Developing

Requirements:

- [VirtualBox](https://www.virtualbox.org/)
- [Vagrant](https://www.vagrantup.com/)

Commands:

- Start the box with `vagrant up`
- Login to the box with `vagrant ssh` and start jekyll with `j`
  (alias to `jekyll serve --incremental --host 0.0.0.0`)
- When done, cleanup with `vagrant destroy`
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

To show a page in the burger menu, tag it with `menu`.
