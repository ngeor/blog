---
layout: post
title: BuzzStats - A new pet project
date: 2010-11-27 19:57:00.000000000 +01:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

This week I've been very busy with my new pet project, BuzzStats.
BuzzStats is an application that collects data from Buzz, a popular social bookmarking Greek speaking community.
<h2>What is Buzz?</h2>

<a href="http://buzz.reality-tape.com/" target="_blank">Buzz</a> is a popular Greek website and community. It's like digg more or less. Users of Buzz can submit new stories, vote stories that other users have submitted, leave comments on existing stories and rate existing comments. The stories are most usual in the Greek language and the topics are often related to politics. I'm not related to the Buzz website in any way, other than being a member.
<h2>What is BuzzStats?</h2>

That's my pet project! A way of extracting data out of Buzz's HTML pages, storing it and displaying cool reports like most popular users, most active day of the week, trending stories, etc.
<h2>Why BuzzStats?</h2>

I started it off as a way of reaching back to my roots, ASP.NET Web Development, and also playing a bit with some toys I wanted to play with. Also because it's cool as a project.
<h2>The Details</h2>

The project consists of two major sub-projects: the Crawler and the Web UI. The Crawler is a console application (at some point it should become a windows service) that periodically reads and parses HTML pages from Buzz in order to extract and store the statistic data. Data are stored in a SQLite database. The Web UI is a read-only ASP.NET frontend to that database, displaying the data. Also, the Web UI exposes some data via a WCF service. The WCF service is consumed by a Silverlight app that displays some nice line series charts using the Silverlight Toolkit.

Since Buzz doesn't offer an API, I had to resort to plain old HTML parsing. Luckily, the HTML contained almost anything I wanted: ids for stories and comments, titles, usernames. Even dates for stories and comments; but no dates for the votes on stories or comments. So I could extract the datetime when a story or a comment was entered, but I could not figure out the datetime when a story or a comment was rated. This problem is solved by polling for changes, as explained below.

I'm quite happy with the architecture on the project. Parser of HTML is separate assembly and so is the Polling logic. The Crawler executable is a mere method call to the Polling logic, so creating a Windows Service to replace the console app will be easy. The Data assembly hides away the underlying NHibernate and exposes three main interfaces for data access: one for write queries (create/update), one for read queries that support caching and one for read queries that cannot be cached. The Crawler uses the write queries and some of the read (always non cached). The Web UI uses the cached read queries only. There's a factory that decides via configuration if caching will actually be used, which is useful for debugging. Also, the cache store is itself abstracted to an interface, in case I want to experiment with memcached later on (so far it's plain old ASP.NET Caching).
<h2>The Algorithm</h2>

In order for BuzzStats to keep itself up to date, it has to periodically poll Buzz and fetch again data. The question is which pages to fetch and when. It is relatively safe to say that by polling the "Most recent stories" page frequently enough, newly entered stories in the system will not go unnoticed. Also, when a user leaves a comment, it will show up in the same page in a separate div so new comment activity can also be detected. But that provides a window of 25 stories maximum (15 recent stories plus 10 most recently commented stories, provided that every recent comment is on a different story and not on recent story). If a user votes on a story outside that window (or rates a comment), it will pass undetected. Therefore, all stories that are known by BuzzStats need to be refreshed from time to time, in order to detect new votes and new comment ratings. But there's another limitation: the number of hits per minute that BuzzStats does needs to be low, to prevent abusing Buzz.

The algorithm I came up with saves together with every story the datetime when it was last fetched from Buzz ( last checked date ) and also the datetime when the story was last found to have new activity ( last active date ). Activity can be a user voting the story, a user commenting on the story, or a user rating a comment of the story. Stories that have been active more recently are more likely to continue to show activity. After some time (perhaps some days), old stories are not visited by users anymore. This makes sense, because articles on Buzz are usually related to current events and the discussion settles down after a while. Therefore it makes sense to use the last activity metric in order to decide which stories to check more frequently.

The algorithm part was very interesting in this project and I have to say that it's still in development. The basic principle is the one described but it has some tweeks here and there (e.g. periodically interrupt the normal flow of the algorithm to re-check the oldest story).

To solve the problem of guessing when a story has been voted, the database contains historical data. Whenever a story is checked, the voters of the story are saved together with the date. The next time the story will be checked, if there are more voters, they will be saved together with the new date. That is the best date that the system can guess as the date when the new votes were cast. For stories that are active and therefore more frequently checked for changes, this approximation will be more accurate. For old stories, if a new vote is found, it will appear to be recent, however it might have been cast a long time ago. That's why the algorithm is so important in this case.

The same applies to rating of comments. The difference here is that comment rating is anonymous in Buzz. Therefore what is being saved is the rating of the comment and the datetime when it was checked. If in the next check the rating has changed, it is reported that at that point the comment got rated. However the actual time when the comment got rated can be in any point between the two checks.
<h2>More Details</h2>

Storing historical data offers interesting opportunities for generating nice and hopefully useful reports on the UI. For example stories can be presented as stocks, some go up fast, some not so fast, etc. That's a part where I haven't focused so much because I've been coping with the more basic stuff (parsing the HTML, figuring out and tuning the update algorithm, etc).

Since I started the project on MonoDevelop, I got to play with some old acquaintances, namely log4net and NHibernate. Actually, I used Fluent NHibernate. It works very nice and you don't have to worry about those hbm.xml files anymore. Together with SQLite that I used for the first time, it worked fine. The database gets generated for me and everything.

When I started playing with Silverlight and WCF, I had to switch over to Visual Studio 2010 Express. There's no Silverlight designer in MonoDevelop, there's no debugging support for Silverlight on the Mac and most importantly, MonoDevelop crashed when trying to generate the web service proxy. That was the end of it.

For the charts I'm using Silverlight Toolkit. It offers some very nice chart controls and in general googling around gives you the answers.

One thing in particular that I learned today was about WCF: there's no HttpContext.Current when you're inside a WCF service call. I was using HttpContext.Current to store the NHibernate session, a <a href="http://www.codeproject.com/KB/architecture/NHibernateBestPractices.aspx" target="_blank">known best practice</a>. After realizing how long it's been since I've used NHibernate and how many things have changed, I found a very <a href="http://www.igloocoder.com/archive/2008/07/21/nhibernate-on-wcf.aspx" target="_blank">cool article</a> that describes how to set it up for WCF. I've put together a reusable assembly that combines both and I plan to publish it on a separate blog article with more details.

One more thing maybe worth blogging about is the auto-detection of the user's timezone. All times in the database are stored in UTC, as usual. However, the Web site user would most likely prefer to view times in his own timezone. The trick is done with a bit of javascript and some redirects. Nothing fancy, but maybe worth showing.
