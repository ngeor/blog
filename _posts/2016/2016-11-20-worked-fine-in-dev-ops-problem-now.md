---
layout: post
title: Worked fine in DEV, OPS problem now
date: 2016-11-20 09:11:50.000000000 +01:00
published: true
categories:
- notes
tags:
- culture
- devops
- technical debt
- notes
---

During the past year at work, we did a complete rewrite of our websites from scratch. Not only did we aim to build a mobile-first responsive website with high performance, we also tried to do it with continuous integration and continuous delivery in mind. All that on a proprietary platform not built with CI in mind. This was a very big challenge, which involved a culture change in a lot of people. Unfortunately, the project had a hard deadline. Things were left out. Corners were cut.

<!--more-->

We did succeed in making one of the fastest websites among its competitors. In many aspects the rewrite was a success. We definitely delivered a better implementation that the previous and this one can grow. To give a hint, the old implementation had no tests whatsoever and people could upload custom code directly on production.

However, people are a bit happier with the result than what they should. Mostly because they judge the success based on the sleek appearance and impressive load times on the frontend. Which reminds me of the following cartoon:

<img src="{{ site.baseurl }}/assets/2016/xxiyrya.png" />

While things are not looking bad on the frontend, our OPS are starting to discover what goes on in the backend. To name a few:
<ul>
<li>no monitoring, especially on third party services</li>
<li>random error logs with poor organization</li>
<li>poor implementation for queue-like operations</li>
</ul>

(We left out a lot more on the backend, but this is what the OPS notice most)

This leads to a lot of manual work for the OPS and a lot of knee-jerk reactions on every incident, leading to ad-hoc panic and overtime.

Some interesting points emerge here:
<ul>
<li>The OPS is an island. Our OPS do a great job as a first line defense. However, they are totally unmanned when it comes to having people fix these things. We do have development teams working on the same platform, but they are working on new business features. OPS has no way of prioritizing a big improvement or a new OPS feature.</li>
<li>Most of these things that OPS are missing were actually planned and thought of in advance. But due to the "Deadline", they were never implemented. This has to do a little bit about technical debt. The business doesn't pay their debt. It is understandable to have a deadline for various reasons. But then continuing on with implementing new features on an effectively half-done platform will lead to problems down the way.</li>
</ul>

At the same time, we have four scrum teams focusing on that platform, creating new business requested features. When they estimate a feature, they won't of course take into account OPS-needed features that are completely missing in the platform. For example, if they're making a new frontend widget, they won't take into account that we need automatic checks for valid HTML, since we haven't build this at all. If they're making a new webservice, they won't take into account that we need live monitoring for the availability of the service on production.

Why do the developers not take these things into account?
<ul>
<li>They don't necessarily have that mindset. Developers often think their job is done when the product owner approves the ticket.<img src="{{ site.baseurl }}/assets/2016/worked-in-dev.jpg" />
</li>
<li>There is no OPS member in the team during planning poker. OPS is an island.</li>
<li>Even if senior developers propose we implement service monitoring, the product owners will be surprised (to say the least), since we never did it before. And they have already a Deadline imposed to them anyway, so this will drop out again and become the technical debt that will not be paid.</li>
<li>The norm is already defined by the existing implementation.</li>
</ul>

How to go about fixing these problems is beyond my knowledge or my responsibility to begin with. But I find these problems interesting as well as painful. I think it is perhaps useful to see what other companies are doing. How are they organizing their teams? What talents are they hiring for? Are developers empowered to work on things they think they have priority? Or are developers passively working solely on business priorities? Do developers have a passion for technology or is it just a job? Does the business understand the importance of having a strong technology culture or is it just a necessity to keep the machine working?

Some of these questions are broad and identity defining for an organization. I have ideas but not answers, in the sense that I don't know what would definitely work.

Back to the OPS challenges, I was thinking of a dedicated team of developers that serves OPS. However this can easily degenerate into a cleanup team, repairing half baked features delivered by the other teams. It doesn't solve the problem at its root. It could solve the problem of repairing existing bad implementations though, without having the OPS frustrated and feeling helpless.

Perhaps what is missing is the DevOps culture. I like test driven development, in which you start with a red test and try to make it green. The software world should come up with a similar methodology in which developers would start implementing a feature by implementing the production sensors that check if the feature is working. Just like you start with a red test in TDD, you should start with a red production OPS alert.

Maybe one day?
