---
layout: post
title: 'CD with Helm part 0: hello world app'
date: 2017-11-13 20:28:56.000000000 +01:00
series:
- CD with Helm
published: true
categories:
- Code
tags:
- blog-helm-sample
- continuous integration
- Docker
- Helm
- Kubernetes
author: Nikolaos Georgiou
---

I'd like to start a tutorial series on how to apply CI/CD principles with tools like Kubernetes and Helm. I'm extremely new in these technologies, so this is a learning exercise for me.

<!--more-->

To kick it off, I need a hello world application which I'll package into a Docker image and deploy it on a Kubernetes cluster with the help of a Helm chart. So, let's start with the hello world application.

It will be a nodeJS application, but that does not matter. I'm following the <a href="https://expressjs.com/en/starter/installing.html" target="_blank" rel="noopener">installing</a> and <a href="https://expressjs.com/en/starter/hello-world.html" target="_blank" rel="noopener">hello world</a> pages of <a href="https://expressjs.com/" target="_blank" rel="noopener">express</a>:

```
mkdir blog-helm
cd blog-helm
npm init
npm install express --save
```

Then, we add the following code to <code>index.js</code>:

```javascript
const express = require('express');
const app = express();
app.get('/', (req, res) => res.send('Hello World!'));
app.listen(
  3000,
  () => console.log('Example app listening on port 3000!'));
```

This gives us a blank application that listens to port 3000 and prints "Hello World!" <a href="https://github.com/ngeor/blog-helm/tree/8efb8a2a74f57b1173a45ae56e371787da6787e4" target="_blank">(browse code)</a>.

I would also like to add some linting with ESLint. The reason for that is to demonstrate later the difference between dependencies and devDependencies and how this affects the build pipeline.

```
npm install eslint --save-dev
./node_modules/eslint/bin/eslint.js --init
? How would you like to configure ESLint? Use a popular style guide
? Which style guide do you want to follow? Airbnb
? Do you use React? No
? What format do you want your config file to be in? JavaScript
```

This will install ESLint as a devDependency and initialize it interactively. I selected the popular Airbnb rules and opted out of the React framework for now.

To run the linter, we can run this command:

```
./node_modules/eslint/bin/eslint.js .
```

But we can also define an npm script in <code>package.json</code>:

```javascript
{
  "scripts": {
    "lint": "eslint .",
```

This allows us to run the linter in this way <a href="https://github.com/ngeor/blog-helm/tree/f70b80c791167a2eef1c542951a00753b48a1671" target="_blank">(browse code)</a>:

```
npm run lint
```

Note that we installed the <code>express</code> framework as a dependency (with <code>--save</code>) but we installed <code>ESLint</code> as a devDependency (using <code>--save-dev</code>). A dependency is a runtime dependency: something that the application will depend upon when it is running. A devDependency is a dependency that the application needs during development but it doesn't need it during runtime (in our case ESLint, but it can also be a unit test framework, some code generator, etc).

It is important to be aware of the difference between dependencies and devDependencies, so that we don't bloat up the runtime dependencies needlessly.

In the next part, we'll have a look at putting the application inside a Docker image (aka dockerize the application).
