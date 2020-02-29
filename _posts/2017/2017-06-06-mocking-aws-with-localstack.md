---
layout: post
title: Mocking AWS with localstack
date: 2017-06-06 20:03:24.000000000 +02:00
published: true
tags:
- aws
- docker
- localstack
- SNS
- SQS
---

We use AWS at work and I've been learning more and more about it. AWS offers so many services it's even difficult to remember all of them. It's quite impressive how many things a developer could build upon in order to deliver a scalable solution. The phrase "standing on the shoulders of giants" is quite fitting.

<!--more-->

Developers are sometimes reluctant to get on board. Why choose DynamoDB when there is MongoDB? Why choose SQS when there is RabbitMQ? Why choose Kinesis when there is Kafka? The list can go on.

The main argument is that these services are managed, which means they are, well, managed by Amazon. You can't get a local copy of SQS and play with it on your computer. You need an AWS account, billing is involved, etc. Also, it's proprietary, and developers tend to favor open source technologies instead.

It's all fine, but there is one factor missing out of this equation: OPS. I've wrote about this <a href="{{ site.baseurl }}/2016/11/20/worked-fine-in-dev-ops-problem-now.html">before</a> and I'm hardly being original by saying that developers often disregard the operational part of the solution. In other words, developers often forget about production and leave it for OPS to sort out.

AWS guarantees a certain availability (I don't remember how many nines). What kind of uptime do your OPS guarantee? Is it even measured? Is there an internal SLA? How stable is your OPS team? How skilled are they? etc What I'm trying to say is, with no disrespect to your OPS team, AWS is probably better. You should be solving the problems of your business and not trying to implement infrastructure at scale (unless of course that is your business).

Using managed services does have another challenge. How do you test your application?

The easiest approach is the old fashioned static DTAP. You have a test environment somewhere. It consists also of dedicated test versions of your AWS managed services. For example, if your application uses SQS, you might have a queue for each environment of the DTAP. The disadvantage of the static DTAP is that it doesn't scale well with CI. To be able to run your tests reliably, you can only run one branch at a time. If you have multiple developers working on multiple branches, each branch will have to wait its turn until the test environment becomes available. That might take a while.

A better approach could be to try and script the creation (and deletion) of the managed services on the fly. Just before running the tests, a script could use the AWS CLI to create a queue. This can create some complexity, because you'll need to have a unique queue name and make the application use that name. There is also a small risk that you'll end up with many queues you're not using if cleaning up is done poorly. And there is also the question of the costs involved.

We live however in the age of containers. It should be possible to dockerize our application together with its dependencies and test it in isolation. Luckily, as it is often the case, somebody has already thought of this and implemented it. In this case, it's Atlassian, who have put together a great Docker image named <a href="https://bitbucket.org/atlassian/localstack/" target="_blank" rel="noopener">localstack</a>.

Localstack is a mock implementation for several AWS services. I've tried it a little bit with SNS and SQS and it seems to work fine (it works on my machine). Each service listens to its own endpoint, for example SNS listens at http://localhost:4575/ and SQS at http://localhost:4576/. To try it out, you just need a small docker compose file:

```
version: '2.1'

services:
  localstack:
    image: atlassianlabs/localstack
    ports:
      - "4567-4582:4567-4582"
      - "8080:8080"
    environment:
      - SERVICES=sqs,sns
      - DEFAULT_REGION=us-east-1

```

And spin it up with <code>docker-compose up</code>.

I have one small tip. If you are going to play with the AWS CLI, you'll need to pass constantly the endpoint URL. I've made some bash aliases to save some keystrokes:

```
alias lsns='aws --endpoint-url=http://localhost:4575 sns'
alias lsqs='aws --endpoint-url=http://localhost:4576 sqs'
```

With this trick, I can type <code>lsns create-topic</code> instead of <code>aws --endpoint-url=http://localhost:4575 sns</code> every time I need a new topic.

This solves the problem of testing in CI with managed services. You dockerize the application, together with localstack and any other dependencies, and you can run as many branches as you want in parallel. For production, you leave out the localstack and use the actual AWS services instead.

I really like the idea behind localstack, but I don't know how reliable it is and how they ensure they're compatible with the actual AWS implementation. In my mind, Amazon should really support this effort and help out e.g. providing sample test suites that localstack should comply to.
