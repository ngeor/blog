# blog

My blog

## Developing

### Local Development

Requirements:

- [VirtualBox](https://www.virtualbox.org/)
- [Vagrant](https://www.vagrantup.com/)

Commands:

- Start the box with `vagrant up`
- Login to the box with `vagrant ssh` and start jekyll with `j`
  (alias to `jekyll serve --incremental --host 0.0.0.0`)
- When done, cleanup with `vagrant destroy`
- Upgrade with `bundle update github-pages`
- Profile with `jekyll build --profile`

### GitPod

- Install with `bundle install`
- Run with `jekyll s --incremental`

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
