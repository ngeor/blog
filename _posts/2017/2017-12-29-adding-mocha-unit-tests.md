---
layout: post
title: Adding mocha unit tests
date: 2017-12-29 18:18:32.000000000 +01:00
published: true
tags:
- blog-helm-sample
- chai
- docker
- mocha
- proxyquire
- sinon
- TeamCity
- Visual Studio Code
---

In this post, I'll add unit tests to the example application that I've been fiddling around with in the recent posts.

<!--more-->

<strong>Folder structure</strong>

In the <a href="{{ site.baseurl }}/2017/12/29/adding-webdriverio-tests.html">previous post</a>, I added some functional tests with WebdriverIO. They were stored in the folder <code>test/specs</code>. I'd like to keep the unit test separate from the functional tests, so I'll rename the old folder to <code>test/functional-specs</code> and store the new unit tests under <code>test/unit-specs</code>.

<strong>Dependencies</strong>

I'll install these dev dependencies (with <code>npm install --save-dev</code>):
<ul>
<li>mocha: the test framework</li>
<li>chai: an assertion library</li>
<li>sinon: a library for spies, stubs and mocks</li>
<li>proxyquire: a library for dependency injection</li>
</ul>

<strong>npm scripts</strong>

I'll setup two npm scripts. One that produces plain text output (for local usage) and one that produces XML report that the CI server can read. This needs to be added to <code>package.json</code>:

```
  "test": "mocha ./test/unit-specs",
  "test-junit": "mocha -R xunit --reporter-options output=test-reports/ci-mocha.xml ./test/unit-specs",
```

Note that the first one works with simply <code>npm test</code> but the second one is invoked with <code>npm run test-junit</code>.

<strong>Adding the first test</strong>

The entire code base consists of a single file, <code>index.js</code>. I'll add a unit test in <code>./test/unit-specs/index.js</code> and I'll unit test the feature provided by the <a href="{{ site.baseurl }}/2017/12/29/waiting-for-the-correct-version-after-deployment.html">version endpoint</a>. You can see the unit test <a href="https://github.com/ngeor/blog-helm/blob/v2.2.2/test/unit-specs/index.js">here</a>.

<strong>TeamCity</strong>

In TeamCity, we need to run the unit tests in the Commit Stage:

```
docker run \
    --rm -v $(pwd)/test-reports:/app/test-reports \
    blog-helm-ci:%env.IMAGE_TAG% \
    npm run test-junit
```

The XML test report gets consumed and the tests are presented in the Test tab:
<img src="{{ site.baseurl }}/assets/2017/12/29/18_12_36-blog-helm-__-commit-stage-_-2-2-2-29-dec-17-16_41-_-tests-e28094-teamcity.png" />

<strong>Visual Studio Code</strong>

One last bit is to configure Visual Studio Code so that I can run and debug the tests from within the editor. Visual Studio Code has a template configuration for running mocha tests and all I had to set is the path where the unit tests live. My entire <code>.vscode/launch.json</code> file is around 30 lines:

```javascript
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "node",
            "request": "launch",
            "name": "Mocha Tests",
            "program": "${workspaceFolder}/node_modules/mocha/bin/_mocha",
            "args": [
                "-u",
                "tdd",
                "--timeout",
                "999999",
                "--colors",
                "${workspaceFolder}/test/unit-specs"
            ],
            "internalConsoleOptions": "openOnSessionStart"
        },
        {
            "type": "node",
            "request": "launch",
            "name": "Launch Program",
            "program": "${workspaceFolder}\\index.js"
        }
    ]
}
```
