---
layout: post
title: Synchronizing App_Data with git
date: 2012-08-26 10:57:00.000000000 +02:00
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

When you have a web application that stores data in it's App_Data folder, at some point you'll want to synchronize the development environment(s) with the live environment. This way your development machine will have the latest live data. This is a task that can be achieved with git.
<h2 id="requirements">Requirements</h2>

I have actually made the following work, but with the following adjustments:
<ul>
<li>All involved Windows machines (development and live boxes) have Cygwin installed</li>
<li>Windows live machine has Cygwin’s open ssh server running</li>
</ul>
<h2 id="step-1---convert-live-appdata-into-a-git-repository">Step 1 - Convert live App_Data into a git repository</h2>

The first step is to convert the App_Data on the live server into a git repository. This will be the source from which all other machines will fetch data from.

To do that, a simple way is to create a new empty git repository, add all existing files, commit and replace the old App_Data folder with the new git repository. Assuming you have a unix (Cygwin) shell, you can write something like:

```
cd /c/web/myapp
mkdir NewAppData
cd NewAppData
git init .
cp -R ../App_Data/* .
git add *
git commit -m "Copying existing App_Data"
cd ..
mv App_Data App_Data.backup
mv NewAppData App_Data
```

At this point the App_Data folder is now a git repository containing all the existing data.
<h2 id="step-2---convert-development-appdata-into-a-git-repository">Step 2 - Convert development App_Data into a git repository</h2>

The second step is to go to the development environment and fetch the App_Data from the production server. Something like:

```
cd /c/projects/myapp
mv App_Data App_Data.backup
git clone ssh://my.live.server/c/web/myapp/App_Data App_Data
```

The local development machine now has a folder C:projectsmyappApp_Data that contains all the live data.
<h2 id="step-3---keeping-up-to-date">Step 3 - Keeping up to date</h2>

As the live server and the development machine continue to work on their App_Data folders, they will reach again a point that they need synchronization. To do that, first you need to commit the changes on the server:

```
git add *
git commit -m "Blindly adding all changes"
```

Next, on the development machine you fetch the changes:

```
git pull
```

That's it.

A bonus step can be automation. By creating scheduled tasks for the commit and pull steps you can stay in sync automatically.

Hope this helps.
