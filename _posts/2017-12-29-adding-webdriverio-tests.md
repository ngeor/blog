---
layout: post
title: Adding WebdriverIO tests
date: 2017-12-29 13:55:32.000000000 +01:00
published: true
categories:
- Code
tags:
- blog-helm-sample
- Docker
- phantomjs
- TeamCity
- WebdriverIO
---

In this post, I'll add some automated browser tests using PhantomJS and WebdriverIO.

<!--more-->

<strong>Add WebdriverIO</strong>

Let's start by adding the <code>webdriverio</code> package as a dev dependency:

```
$ npm install --save-dev webdriverio
```

Next, we need to setup the initial configuration with:

```
$ ./node_modules/.bin/wdio config
```

This starts a configuration wizard with some questions:
<ul>
<li><em>Where do you want to execute your tests?</em> On my local machine</li>
<li><em>Which framework do you want to use?</em> mocha</li>
<li><em>Shall I install the framework adapter for you?</em> Yes</li>
<li><em>Where are your test specs located?</em> <code>./test/specs/**/*.js</code></li>
<li><em>Which reporter do you want to use?</em> dot, junit</li>
<li><em>Shall I install the reporter library for you?</em> Yes</li>
<li><em>Do you want to add a service to your test setup?</em> phantomjs</li>
<li><em>Shall I install the services for you?</em> Yes</li>
<li><em>Level of logging verbosity</em> silent</li>
<li><em>In which directory should screenshots gets saved if a command fails?</em> <code>./errorShots/</code></li>
<li><em>What is the base url?</em> <code>http://localhost:3000</code></li>
</ul>

I mostly left the default options. I changed the reporter to include junit, because I want to consume the report in the CI server. I also added the phantomjs service because I don't want to set that up by myself.

<strong>Add the first test</strong>

Now that WebdriverIO is configured, I can add an example test:

```javascript
const assert = require('assert');

describe('homepage', () => {
  it('should have the correct title', () => {
    browser.url('/');
    const title = browser.getTitle();
    assert.equal(title, 'blog-helm');
  });
});
```

Small note: the <a href="{{ site.baseurl }}/2016/06/25/functional-testing-hello-world.html" target="_blank">last time I dove into WebdriverIO</a>, things were a bit more complicated, with promises and callbacks. Now all that seems to be hidden away.

<strong>Run the tests</strong>

To run the tests, we can run <code>./node_modules/.bin/wdio</code>. Since we're using npm scripts, I'll add an npm script for this as well in <code>package.json</code>:

```
  "scripts": {
    "lint": "eslint .",
    "lint-junit": "eslint -f junit -o test-reports/eslint.xml .",
    "test": "npm run lint",
    "start": "node index.js",
    "wdio": "wdio"
  }
```

This way we can run them with <code>npm run wdio</code>.

For the junit reporter to work, we need to configure its output directory. That's done in the <code>wdio.conf.js</code> configuration file:

```
  reporters: ['dot', 'junit'],

  reporterOptions: {
    junit: {
      outputDir: './test-reports',
    },
  },
```

<strong>Configure CI</strong>

I'd like to be able to run these tests on any environment after the deployment has succeeded. This requires the dev dependencies (webdriverio and friends), which are in the CI image we use to run linting and unit tests, which isn't published to the docker registry. The first step therefore is to publish the CI image to the docker registry during the Commit Stage, so that it's available in the Deployment build configurations.

With that in place, I can run the tests like this:

```
docker run \
    --rm -v $(pwd)/test-reports:/app/test-reports \
    blog-helm-ci:%build.number% \
    npm run wdio -- -b %app.baseurl%
```

Notice that I'm passing the base URL I configured in the <a href="{{ site.baseurl }}/2017/12/29/waiting-for-the-correct-version-after-deployment.html">previous post</a> in the %app.baseurl% configuration parameter. This way the tests run against the correct environment.

<strong>PhantomJS problems with Alpine</strong>

While in theory this should've worked, it didn't. PhantomJS did not run. The reason had to do with the Docker image. It was based on Alpine, which is not supported by PhantomJS. The easiest workaround was to switch to the <code>slim</code> flavor, which works. As this is only the CI image and not the production image, I think it's okay.

<strong>Results</strong>

In the end, we can see that we have the new test passing on all environments:

<img src="{{ site.baseurl }}/assets/2017/12/29/14_07_21-blog-helm-__-deploy-to-production-_-build-chains-e28094-teamcity.png" />

And we can see the test title in the test report too:

<img src="{{ site.baseurl }}/assets/2017/12/29/14_07_49-blog-helm-__-deploy-to-test-_-2-0-0-29-dec-17-13_05-_-tests-e28094-teamcity.png" />
