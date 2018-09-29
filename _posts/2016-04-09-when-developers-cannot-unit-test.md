---
layout: post
title: When developers cannot unit test
date: 2016-04-09 08:27:00.000000000 +02:00
parent_id: '0'
published: true
categories:
- Tech Notes
tags:
- code review
- knowledge sharing
- pair programming
- unit tests
author: Nikolaos Georgiou
---

Unit tests is an essential method of ensuring quality and predictability of software. In my current work, we have been going through a hard learning curve involving many factors:
<ul>
<li>developers not familiar with unit tests.</li>
<li>a proprietary technology ecosystem where the community is typically not practicing unit tests at all.</li>
<li>a legacy code base not written with unit tests in mind</li>
</ul>

<!--more-->

When developers are not familiar with unit tests, you have to first <strong>convince them that unit tests have value</strong>. Developers are known to have poor communication skills, so communicating and convincing can be challenging. They're also known to hold on to their opinions, defend bad practices due to their 'experience', and other ego-related issues. In the end, you may need a higher power to help. I'm not talking about religion but getting management buy-in.

In my case I was lucky to have developers willing to learn and I didn't have to waste any energy futile. But, willingness doesn't beat habit. Every now and then, <strong>people will simply forget</strong> about writing unit tests. It is expected and understandable. If you've never written unit tests before, you'll tend to forget about it. How do we deal with this? We try to keep an eye out during <strong>code reviews</strong>. A tip I tell people is to just look at the filenames in a pull request (PR). Don't even go to the code itself, just look at the listing of the filenames. If a code file is affected in a PR but its corresponding unit test isn't, then 90% of the time it means the author forgot to create or amend the unit tests. <strong>Code coverage</strong> also helps here, but only assuming your threshold is close to the actual coverage. If your coverage is at 80% and your threshold is 70%, you don't want to lose a 10% investment before you figure out that people are not writing tests.

When you're working on a <strong>proprietary platform with no unit test culture</strong>, hiring the ideal developer is practically impossible. Somebody who knows the platform very well will probably have never written a unit test, because nobody writes unit tests in this platform. (Side note: This culture leads to what a friend of mine calls the <strong>web agency bingo</strong>. The client hires a web agency, for a while everything is fine, then bugs accumulate, the client is unhappy, picks another web agency with new hopes and the game starts over). Depending on the existing skills of the team, you hire for what it takes less time to train for, there's no silver bullet here. You can do <strong>pair programming</strong> and <strong>knowledge sharing sessions</strong> to help reduce imbalances in the skills of the team. That will take time (which, depending on priorities, it may be a luxury).

But the biggest problem of all is teaching <strong>how to write a good unit test</strong>. I think that a lot of this comes with experience and it is subjective up to a certain extent.

In the following weeks, I'll try to write some posts about:
<ul>
<li>what is a unit test and what is a unit</li>
<li>what is test driven development</li>
<li>how to deal with dependencies</li>
<li>avoiding evergreen tests</li>
<li>testing behavior and not implementation</li>
<li>if a developer writes tests, what is the role of the QA engineer</li>
</ul>

and similar topics. I hope that by writing these things down, I'll clear them a bit in my head and then I'll become a bit better in explaining them to others.
