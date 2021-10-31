---
layout: page
title: Project checklist
date: 2021-10-31
---

Setting up a project, creating a pipeline, automatic deployments, etc.

## Getting all projects

List all your projects with [instarepo]:

```sh
pipenv run python -m instarepo.main -u [USER] -t [TOKEN] --no-forks list
```

Clone them all with a bit of bash magic:

```sh
for repo in $(pipenv run python -m instarepo.main -u [USER] -t [TOKEN] --no-forks lis
t | cut -d\  -f1); do echo git clone git@github.com:[USER]/${repo}.git /tmp/ ; done
```

To get latest version of all repositories under a common projects folder,
you can use another bash script:

```sh
for repo in $(ls); do pushd ${repo} ; git pull ; popd ; done
```

## Project checklist

The following files must exist:

- `README.md`
- `.gitignore`
- `.editorconfig`

If this is a library:

- `CHANGELOG.md`

Regarding CI, .NET projects should use [AppVeyor],
other projects should use [GitHub Actions].

## Badges

TODO

## Bumping version

TODO


[instarepo]: https://github.com/ngeor/instarepo
[AppVeyor]: https://ci.appveyor.com/
[GitHub Actions]: https://github.com/features/actions
