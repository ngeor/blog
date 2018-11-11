---
layout: page
title: Upgrading Dependencies
---

This page shows how to upgrade dependencies in various programming languages
and dependency management systems.

## node - npm - npm-check-updates

Prerequisite: install [npm-check-updates](https://www.npmjs.com/package/npm-check-updates) with `npm install -g npm-check-updates`.

To upgrade your dependencies run `ncu -u`. More options are available in the
documentation.

## Python - Pip - Pur

You have a `requirements.txt` file with your dependencies.

Prerequisite: install [pur](https://pypi.org/project/pur/) with `pip install
pur`.

To upgrade your dependencies: `pur -r requirements.txt`
