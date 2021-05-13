---
layout: post
title: Using Lerna for TypeScript and npm
date: 2021-05-13 07:08:32
tags:
  - lerna
  - monorepo
  - typescript
  - npm
---

In this post, I'm showing a way to setup a monorepo with Lerna, taking into
account some pitfalls when publishing to npm.

[Lerna](https://github.com/lerna/lerna) is a tool for managing JavaScript
projects with multiple packages. In my very simple example, I have a project
with 3 packages: a library, a CLI, and a VS Code Extension. The library package
is used by both the CLI and the VS Code Extension packages.

Lerna makes the following things easy in my workflow:

- Linking dependent packages together for local development. Normally, you'd
  have to use the `npm link` command (multiple times, depending on how many
  packages you need to link). With Lerna, `lerna bootstrap` takes care of that
  when you first clone a project (together with doing `npm install` for you).
- Version management. Conceptually, my packages are all part of the same
  project, so I would like all of them to have the same version. Lerna takes
  care of that easily, the version is declared in the `lerna.json` file and
  controls the version for all packages. Bumping the version is also easily done
  with the `lerna version` command.
- Publishing to npm. For my workflow, I like to publish all packages to npm,
  even if they didn't have any changes since the previous release. I'll dive
  into npm publishing in more details later, but this is done in two steps. On
  my local machine, I use the `lerna version` command to bump the version. This
  creates and pushes a git tag. On the CI side, I run the `lerna publish`
  command whenever a new tag is pushed.

## Repo structure

Things get a bit more complicated because I use TypeScript instead of
JavaScript. I'm going to show a little bit the structure of my repo:

```
[packages]
  |- [html-fmt-cli]
  |    |- [src]
  |    |    |- index.ts
  |    |    \- index.test.ts
  |    |- package.json
  |    |- tsconfig.json
  |- [html-fmt-core]
  \- [html-fmt-vscode]
README.md
lerna.json
package.json
```

On the top level, there's the root `package.json` and `lerna.json` files. The
root `package.json` just lists Lerna as a dev dependency. It's flagged as
private to prevent accidentally publishing this to npm. `lerna.json` holds the
version of the packages and indicates that packages are to be found under the
`packages` folder.

The three packages underneath the `packages` folder have a similar structure.
Inside you'll find a `package.json` and a `tsconfig.json`. To avoid mixing the
code with other files, code is kept in a separate sub-directory, `src`. This
will make life a bit more complicated when publishing to npm, which I'll discuss
later. Tests are kept side by side with the code they're testing (e.g.
`index.test.ts` is the unit test file for `index.ts`). I like this option more
compared to keeping tests on a separate directory because it's easy to locate
and easier to write the `import` statement without trying to figure out how many
`../` to add to match the directory structure.

## tsconfig

Moving further to TypeScript, this is how my `tsconfig.json` looks like for the
library project, `html-fmt-core`:

```json
{
  "compilerOptions": {
    "declaration": true,
    "outDir": "./out",
    "allowJs": false,
    "target": "es6",
    "module": "commonjs",
    "moduleResolution": "node",
    "sourceMap": true,
    "strict": true
  },
  "include": ["src/**/*.ts"]
}
```

The key elements here are:

- Source code is in `src` folder
- Output JavaScript code will be in `out` folder (sibling of `src`)
- Generate declaration files (`"declaration": true`), this makes VS Code happy

## Main script and subdirectories

This brings us to the next point, specifying the entry point in `package.json`:

```json
{
  "main": "out/index.js"
}
```

The complications start from the fact that the main file is in a subdirectory.
Let's say that `index.js` exports a function named `hello`. You can use it in a
different package like you would expect:

```js
import { hello } from "html-fmt-core";
```

Let's say now that we have a file named `Formatter.ts` (compiled into
`Formatter.js`).

You would expect this might work:

```js
import { whatever } from "html-fmt-core/Formatter";
```

but unfortunately it doesn't. What does work is specifying the `out` directory:

```js
import { whatever } from "html-fmt-core/out/Formatter";
```

To avoid this altogether, what I did is to re-export what I want in the
`index.ts` file like this:

```js
export * from "./Formatter";
```

and use it as if it was part of the index file:

```js
import { hello, whatever } from "html-fmt-core";
```

Note that this complication is happening because I've got the source code in the
`src` folder and the generated code in the `out` folder. It is also possible to
avoid this pain by simply having the code at the root level of the package (side
by side with `package.json` and `tsconfig.json`) and output the generated code
also there (with some rules in `.gitignore` to avoid committing it to git
accidentally).

## Publishing to npm

As I said in the beginning, it's easy to publish all lerna packages with one
command. With my current setup, I will have some problems:

- It will publish not only the JavaScript code but also the TypeScript code. I
  would like it to publish only the JavaScript code (together with the
  declaration files for TypeScript users). This can be solved with some
  `.npmignore` lines but I'll do it a bit differently.
- It will publish not only the code, but also the tests.
- My `README` file will be missing, because it's at the root folder of the
  _project_ and I don't have (and don't want to have) a `README` per _package_.

The thing is, my JavaScript code is already nicely contained in the `out`
folder, so I'd like to publish just that subdirectory. Lerna
[supports this](https://github.com/lerna/lerna/tree/main/commands/publish#--contents-dir),
with a very spot on description:

> If you're into unnecessarily complicated publishing, this will give you joy.

So as per the docs, I need to write a custom script that will run in the
`prepack` step and:

- create an artificial `package.json`
- copy the `README.md` from the project root into the generated package root

My custom prepack script looks like this:

```js
const fs = require("fs");

fs.copyFileSync("../../README.md", "out/README.md");

if (fs.existsSync(".npmignore")) {
  fs.copyFileSync(".npmignore", "out/.npmignore");
}

let packageJson = JSON.parse(
  fs.readFileSync("package.json", { encoding: "utf8" })
);
packageJson.main = "index.js";

if (packageJson.bin) {
  packageJson.bin = "index.js";
}

packageJson.scripts = {};
fs.writeFileSync("out/package.json", JSON.stringify(packageJson));
```

- It copies over the README file from the project root into the output folder of
  the package
- If an `.npmignore` file exists on the package root, copy it over to the out
  folder (I use the `.npmignore` file to ignore the tests)
- Create an `out/package.json` based on the original with the following
  alterations:
  - the main entry point will be `index.js` instead of `out/index.js`
  - same for the `bin` script, if one exists (it exists for the CLI project)
  - clear out the `scripts` because why not

The publish command for this is `lerna publish -y --contents out from-package`.

## Summary

Looking back at this, perhaps the easiest way is to leave the TypeScript code at
the package root and let the output JavaScript code live there too. However, if
you like to have a separate source subdirectory and a separate output
subdirectory, it's definitely possible, with a bit of extra work.
