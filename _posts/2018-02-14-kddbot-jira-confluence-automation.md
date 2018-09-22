---
layout: post
title: 'kddbot: JIRA -> Confluence automation'
date: 2018-02-14 15:45:54.000000000 +01:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags:
- AWS
- AWS Lambda
- Confluence Cloud
- JIRA Cloud
- kdd
- kddbot
- python
author: Nikolaos Georgiou
---

TL;DR: I implemented a small working poc that shows how to automatically create a Confluence page when a Jira ticket is created.

<!--more-->

<strong>Background</strong>

At work, we try to make decisions in a transparent way, weighing pros and cons, capturing the process of deciding in Confluence, for everyone to be able to look back to. We call this a <strong>Key Decision Document</strong> (KDD for short).

For example, there might be a need to pick between two frameworks like React and VueJS. Instead of letting the loudest person win, or selecting based on arbitrary past experiences or preferences, or having a group of people discuss it in a room (and leave thinking they have agreed but they have actually different opinions), we write everything down in Confluence.

From an administrative point of view, we need:
<ul>
<li>one Jira ticket to work on the KDD</li>
<li>the actual KDD page in Confluence</li>
<li>the Jira ticket needs to be linked to the KDD page</li>
</ul>

There's actually quite a few clicks involved in doing that, which is boring and error prone. So I wrote some code that gets called when someone creates a Jira ticket and creates the blank KDD page.

<strong>The code</strong>

The code is on GitHub with the imaginative name <a href="https://github.com/ngeor/kddbot">kddbot</a> and an equally fancy logo (I combined two free images together). It is basically an AWS Lambda function written in Python (new year resolutions). The README file has sufficient technical information on how to set it up if you're interested.

<strong>Lessons and thoughts</strong>

Confluence has a blueprint for this type of documents. When doing this manually, you click "Create Page" in Confluence and you select the "Decision" blueprint. I was surprised to see that the REST API doesn't offer this functionality. For the time being, you cannot programmatically create a page in Confluence based on a blueprint. As a workaround, I hardcoded the contents of the blueprint in the Python code (so now the template HTML lives both in Confluence and in my code).

I think that the REST API should be actually a first class citizen. The principle here is "<a href="https://en.wikipedia.org/wiki/Eating_your_own_dog_food">eat your own dog food</a>". The API you expose to your customers would probably have more features and might be better documented if everyone who wants to use your features must go via that API, even for projects within your organization. It shouldn't happen as an afterthought, because it might be more difficult to impement.

Using a tool like Postman was quite handy in implementing this poc. For example, it's not clear what happens under the hood when I link a Jira ticket to a Confluence page. This isn't explicitly documented in the API. Poking around Postman on existing tickets reveals that this type of link is a "remote link". The same observation applies to using Confluence macros, like Status, Page Properties, etc. I couldn't find any documentation, so the easiest way was to see what markup was being used on an existing page.

I like working with Lambda functions (I don't have much experience with it) because now I have a working integration which is always there, without requiring permanent infrastructure. The way of implementing it was fun, fast, but also hacky. I'd like to learn more about how I should test such a function, deploy it automatically, etc. It is however very liberating to see results with just a few lines of code.
