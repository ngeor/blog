---
layout: post
title: npm login credentials on the CI server
date: 2017-01-28 08:37:30.000000000 +01:00
parent_id: '0'
published: true
categories:
- Code
tags:
- continuous integration
- JavaScript
- npm
author: Nikolaos Georgiou
---

In a <a href="{{ site.baseurl }}/2016/08/20/automatic-versioning-of-npm-packages.html">previous post</a>, I was discussing a way to publish an npm package to the public npm registry. A big prerequisite for that to work is that you have previously logged in to the CI server in order to authenticate against npm. But we can also fix that manual step and integrate it in the build.

<!--more-->

When you login to npm, a file <code>.npmrc</code> is generated and stored in your home directory. This file contains an authentication token. We're going to login to a regular developer's machine, generate that authentication token and then store it CI as a parameter. Defining a parameter in CI is something that typically requires far less privileges compared to a full shell login to the CI server itself.

First, login to npm with the <code>npm login</code> command. It goes like this typically:

```
$ npm login
Username: john.doe
Password: ********
Email: (this IS public) john.doe@company.com
Logged in as john.doe on https://registry.npmjs.org/.
```

This generates the file we need, <code>.npmrc</code>, which looks like this:

```
$ cat .npmrc
//registry.npmjs.org/:_authToken=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

The authentication token is basically a GUID that npm provides. If this file is present on another machine (e.g. the CI server), then you can publish to npm from that machine. This token should be therefore treated as a password, as far as security is concerned.

You don't even need access to the CI server or bother your OPS with that. Since the file format is very simple and straightforward, you can generate it on the fly during the build. Implement a build step that consists of this simple bash script:

```
#!/bin/bash
cat < .npmrc
//registry.npmjs.org/:_authToken=$NPM_AUTH_TOKEN
EOF
```

This script generates the <code>.npmrc</code> file, using the environment variable <code>NPM_AUTH_TOKEN</code>. All you have to do now is to define that environment variable in your build configuration.

