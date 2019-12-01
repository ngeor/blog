---
layout: post
title: Adding code coverage with nyc
date: 2017-12-29 19:07:25.000000000 +01:00
published: true
categories:
- testing
tags:
- blog-helm-sample
- code coverage
- Docker
- nyc
- TeamCity
---

In this post, I'll add code coverage to the build pipeline and configure TeamCity to break the build if the code coverage drops.

<!--more-->

<strong>Installation</strong>

The tool we'll use is <a href="https://github.com/istanbuljs/nyc">nyc</a> and it's installed simply as a dev dependency with <code>npm install --save-dev nyc</code>.

<strong>npm scripts</strong>

I'll also add two npm scripts in <code>package.json</code>:

```
"nyc": "nyc npm test",
"nyc-junit": "nyc npm run test-junit"
```

They both use the npm scripts configured in the <a href="{{ site.baseurl }}/2017/12/29/adding-mocha-unit-tests.html">previous post about unit tests</a>. The second one produces the unit test XML report, so it will be used on the build server.

<strong>Configuring nyc</strong>

nyc can be configured by adding a <code>nyc</code> element in <code>package.json</code>:

```javascript
  "nyc": {
    "all": true,
    "reporter": [
      "text",
      "html",
      "teamcity"
    ],
    "exclude": [
      "wdio.conf.js",
      "coverage/**/*.js",
      "test/**/*.js"
    ]
  }
```

I'll explain a bit my configuration:
<ul>
<li><code>"all": true</code> specifies that the code coverage should include source code that is not referenced via unit tests. This is not the default, which I personally find odd. Without this flag, it's possible to keep adding code without unit tests and you'll never notice a drop in the code coverage. I prefer to calculate the code coverage for all source code, so that if unit tests are missing, the build will break.</li>
<li>I use three reporters: text, html and teamcity. The first one prints a short summary table to the console, which is the default behavior. The second one generates a HTML report in the <code>coverage</code> folder. You can use this report to see what you have covered and what you're missing. That last reporter sends the code coverage metrics to TeamCity.</li>
<li>The exclude array indicates files I don't want to calculate in the code coverage. That's the configuration of WebdriverIO, the tests and the code coverage report.</li>
</ul>

<strong>Results</strong>

This is how the HTML report looks like on a file level (I only have one file to test in the sample project anyway):

<figure><img src="{{ site.baseurl }}/assets/2017/12/29/18_47_19-code-coverage-report-for-index-js.png" /><figcaption>HTML coverage report</figcaption></figure>

As I said in the previous post, I only added a unit test for the <code>/version</code> endpoint, so the other two functions are not covered and appear with a red-pink color.

In TeamCity, the code coverage metrics are visible on the Overview tab:

<figure><img src="{{ site.baseurl }}/assets/2017/12/29/18_50_05-blog-helm-__-commit-stage-_-2-2-2-29-dec-17-16_41-_-overview-e28094-teamcity.png" /><figcaption>TeamCity code coverage summary</figcaption></figure>

<strong>Failure conditions</strong>

It is possible to configure nyc to break the build when the code coverage drops under a certain fixed value. TeamCity allows you to take a different approach: break the build if code coverage drops by a certain amount compared to the previous successful build:

<figure><img src="{{ site.baseurl }}/assets/2017/12/29/17_28_32-commit-stage-configuration-e28094-teamcity.png" /><figcaption>TeamCity failure condition gives dynamic thresholds</figcaption></figure>

This is great if you have a project with a low code coverage and you are determined to improve it. Every green build sets automatically the bar higher, without having to manually update the thresholds:

<figure><img src="{{ site.baseurl }}/assets/2017/12/29/19_03_57-blog-helm-__-commit-stage-_-2-2-3-drop-coverage-2-29-dec-17-18_02-_-overview.png" /><figcaption>Broken build due to lower coverage</figcaption></figure>
