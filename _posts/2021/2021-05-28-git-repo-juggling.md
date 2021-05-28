---
layout: post
title: Git repo juggling
date: 2021-05-28 12:02:59
tags:
  - git
  - monorepo
  - multirepo
---

This post shows how to use `git subtree` commands to move git repositories around.
Perfect if you're indicisive about monorepo vs multirepo.

## Move a repo in a different repo as a subfolder

Use case: you want to move a library into a monorepo (because you read a post that says it's cool).

Before:

```
Source repo             Destination repo
|                       |
|-- src                 |-- packages
|   \-- index.ts        |   \-- bar
|-- package.json        \-- README.md
|-- package-lock.json    
\-- README.md
```

After:

```
Destination repo
|
|-- packages
|   |-- bar
|   \-- foo (**moved here from source repo**)
|       |-- src
|       |   \-- index.ts
|       |-- package.json
|       |-- package-lock.json
|       \-- README.md
\-- README.md
```

Steps:

- Clone the source repo in a folder named `source`
- Clone the destination repo in a sibling folder named `destination`
- In the destination repo, run: `git subtree add -P packages/foo ../source master` (assuming the main branch is called `master`)
- Delete the source repo (I'm sure you won't regret it)

## Move a subfolder to a new repo

Use case: you want to move a library out of a monorepo into its own dedicated repo
(because you read a different post that says monorepos are actually not cool).

Before:

```
Source repo     
|
|-- packages
|   |-- bar
|   \-- foo
|       |-- package.json
|       \-- README.md
\-- README.md
```

After:

```
Destination repo (**keeping only the contents of foo**)
|-- package.json
\-- README.md
```

Steps:

- Clone the source repo in a folder named `source`
- Prepare a new empty **bare** repo in a folder named `destination` (with `git init --bare`)
- In the source folder, run `git subtree push -P packages/foo ../destination master`
- To double check everything went fine, you can clone the bare repo into a regular repo and inspect
  its contents.
- Delete the library from the source repo  

## Move a subfolder to an existing repo

Use case: you have two monorepos and you want to move one library from one to the other
(because the oxymoron of having multiple monorepos escapes you).

Before:

```
Source repo    Destination repo
|              |
|-- packages   |-- libs
    |-- bar        \-- bar
    \-- foo       
```

After:

```
Source repo    Destination repo
|              |
|-- packages   |-- libs
    \-- foo        |-- bar
                   \-- bar_v2 (** moved here from source repo where it was called bar **)
```

- Clone the source repository into a folder named `source`
- Clone the destination repository into a sibling folder named `destination`
- In the source repo, keep only the desired library with `git subtree split -P packages/bar -b temp` (temp is the name of a branch we'll use next)
- Checkout the `temp` branch and double check the source repo folder only has the desired library
- In the destination repo, add the library with `git subtree add -P libs/bar_v2 ../source temp`
- Delete the library from the source repo  
