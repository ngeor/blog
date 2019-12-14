---
layout: page
title: Upgrading Dependencies
date: 2018-11-04
---

This page shows how to upgrade dependencies in various programming languages and
dependency management systems.

## Java - maven - versions maven plugin

See
[here](https://www.mojohaus.org/versions-maven-plugin/examples/display-plugin-updates.html)

- To check if there are dependency updates:
  `mvn versions:display-dependency-updates`
- To check if there are plugin updates: `mvn versions:display-plugin-updates`

## node - npm - npm-check-updates

Prerequisite: install
[npm-check-updates](https://www.npmjs.com/package/npm-check-updates) with
`npm install -g npm-check-updates`.

To upgrade your dependencies run `ncu -u`. More options are available in the
documentation.

## Python - Pip - Pur

You have a `requirements.txt` file with your dependencies.

Prerequisite: install [pur](https://pypi.org/project/pur/) with
`pip install pur`.

To upgrade your dependencies: `pur -r requirements.txt`
