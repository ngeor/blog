---
layout: post
title: 'Fun project: HipChat integration with AWS Lambda'
date: 2017-04-12 19:19:35.000000000 +02:00
published: true
categories:
- tech
tags:
- aws
- atlassian
- CloudWatch
- continuous integration
- aws lambda
- travis
---

TL;DR: I made a [hobby project](https://gist.github.com/ngeor/bb13c0d2937769fb71bd912664d073aa)
that gets the pull requests that still need code reviews from Bitbucket and posts a notification message on HipChat to inform developers. It's written in JavaScript (nodeJS). Travis CI automatically deploys it to AWS as a Lambda function. AWS CloudWatch is used to trigger the function hourly.<!--more-->

Hobby projects are a fun way to learn something new. In this case it started by curiosity. I noticed that HipChat, the group chat that we use at work, has an Integrations menu that allows you to connect to third party services:

<img src="{{ site.baseurl }}/assets/2017/hipchat.png" />

Even more interestingly, if you follow the menu, the first available integration is called "Build your own":

<img src="{{ site.baseurl }}/assets/2017/hipchat2.png" />

Now, that sounds like an invitation to a party to my ears. When you click this link, it asks you to name your integration and that's it:

<img src="{{ site.baseurl }}/assets/2017/hipchat31.png" />

You get a URL with an authentication token and you're ready to start posting messages to that URL.

Then I asked myself: what could I post to my team's HipChat group that could actually be useful? Well one thing we have is that people often post messages saying "please review my pull request". I thought that that could be something that we can automate.

I created a prototype project that connects to Bitbucket's API and gets open pull requests for a set of git repositories. For every pull request, we require at least 2 approvals. If a pull request has less than two approvals, the script uses the HipChat URL to post a "please review" message:

<img src="{{ site.baseurl }}/assets/2017/hipchat41.png" />

This just a PoC so I don't have unit tests and the code base is more or less contained in a single file (~150 lines). Knowing that it can't get much bigger than this, and because I wanted to play a bit with AWS Lambda as well, I implemented it as an AWS Lambda function. You get started off with an easy template and you can edit the code directly in the AWS Lambda UI:

<img src="{{ site.baseurl }}/assets/2017/lambda.png" />

You can also use node modules, but you'll have to upload a zip file containing everything. I definitely needed the request module in order to call Bitbucket.

The zip file complicated things and I ended up doing a bit more plumbing work. I had to setup a basic grunt pipeline that runs my linting, unit tests (I added one) and produces a zip file that contains my code and the production dependencies. I don't want to upload to AWS the devDependencies, such as grunt, mocha, etc. That last part was a bit tricky. I didn't find a built-in node or npm way to do this, so I improvised. I copy my package.json in a temp folder and I run <code>npm install --production</code> there. It does the trick and I have my rudimentary CI pipeline, generating a zip file as an artifact.

I was pleased to see that my CD pipeline was actually a freebie by Travis. Travis supports deploying to AWS Lambda out of the box. So as soon as I commit something to my repository, CI produces my zip file and CD uploads the new version to AWS. If Travis didn't offer this, I'd have to use the AWS CLI on my own.

<img src="{{ site.baseurl }}/assets/2017/lambda2.png" />

The last part is the schedule. I'd like to invoke my function automatically every hour, with a cron like system. In AWS, you can use a CloudWatch event rule for this. It's more friendly that it sounds and when you configure the Lambda's triggers, it actually gives this as a possible trigger. I think in general the UX of the AWS website is quite friendly and it guides you well.

<img src="{{ site.baseurl }}/assets/2017/cloudwatch.png" />

This entire thing from begin to end didn't take more than a few hours. Editing and running the code directly in the browser is quite fun.

Next steps: one idea is to also connect to the TeamCity API and check if the PR has actually a green build. If it has a red build, it can inform the developers to ignore that PR for example.

It can also check how old a pull request has been open and if it's open for more than 3 days then it should use a red color for the HipChat notification.

Also, I noticed that HipChat offers commands for the integration. This can turn the HipChat integration into a bot, replying to user's commands:

<img src="{{ site.baseurl }}/assets/2017/hipchat5.png" />

So maybe instead of having an hourly schedule, a developer can instead type "/reviews" and the Lambda can reply back a list of PRs that need a review. It can even reply a more personalized message, excluding PRs for which the user is the author (assuming here that Bitbucket and HipChat usernames are identical or have a known mapping).

Hacking is fun, because hacking is learning.
