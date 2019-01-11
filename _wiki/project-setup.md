---
layout: page
title: Project Setup
---

Setting up a project, creating a pipeline, automatic deployments, etc.

Creating a project
------------------

Simply create the project on GitHub. Select the appropriate `.gitignore`
template and license (typically MIT).

Add a common `.editorconfig` file.

Enable the project via the Travis UI.

Deployment Options
------------------

There are two deployment options:

- Deploy on tag
- Deploy on master

Bumping Version
---------------

### Bumping Version with npm

`npm version minor` and `npm version patch` are useful commands that ensure that
there are no gaps in SemVer. They create a separate commit for the version bump,
together with a tag. It is possible to combine it with a `postversion` npm
script which will push the tag (e.g. `git push --follow-tags`)

This utility makes the **Deploy on tag** option easy to implement.
