---
layout: post
title: Thinning ZFS snapshots
date: 2016-09-03 07:28:21.000000000 +02:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags:
- backup
- zfs
author: Nikolaos Georgiou
---

I have a small mini PC at home that is always turned on. It runs Ubuntu 14.04 (I plan to upgrade to 16.04). It sits at the living room and it doesn't make any noise, so it acts as a media server. I watch movies and TV series from there. I used 3 external disks, 2TB each, to make a ZFS raidz1 pool of 4TB. What is ZFS you ask?<!--more-->

<a href="https://en.wikipedia.org/wiki/ZFS">ZFS</a> is a file system that can combine multiple drives and make them appear as one. It will figure out where the files go, all you know is that you have one big bucket to throw data in. This can be done in various configurations to give you extra security in case a drive fails. So in my case, I have setup a raidz1 pool. This means that if one disk fails, the system will continue to operate. If two disks fail, well, everything is lost. But I guess the chances of two disks failing are way higher than one disk. This also means that instead of 6TB (3 disks of 2TB), I have only 4TB available. But so far that's enough for me.

Another nice feature of ZFS is snapshots. You can take a snapshot of the file system at a given point and rollback to it later. Snapshots are cheap too. I use them as a method of backup. I have setup a cron job that runs every day and takes a snapshot of the file system. The snapshot is identified by its name, so I use a script for that to make sure all the snapshot names are basically a timestamp:

```
#!/bin/sh

# put zfs on the path
PATH=$PATH:/sbin

# takes a snapshot on the given filesystem
# the snapshot name is the current date

SNAPSHOT_NAME=`date +%Y%m%d%H%M%S`
FILESYSTEM=$1

if [ -z $FILESYSTEM ]; then
	echo "Syntax $0 filesystem"
	return 1
fi

SNAPSHOT_LIST=`zfs list -H -o name -t snapshot -r $FILESYSTEM | sort`
if [ ! $? -eq 0 ]; then
	echo "zfs failed"
	exit 1
fi

if [ -z "`echo $SNAPSHOT_LIST | grep $SNAPSHOT_NAME`" ]; then
	zfs snapshot $FILESYSTEM@$SNAPSHOT_NAME
else
	echo "Snapshot $FILESYSTEM@$SNAPSHOT_NAME already exists"
	exit 1
fi
```

A problem here is that the disk space reserved by snapshots will start to accumulate over time. I've been running this for almost two years now and that's a lot of snapshots. I decided to make a small script that will automatically thin out older snapshots. The rules are simple:
<ul>
<li>for the current month, don't delete anything</li>
<li>for previous months of this year, keep only one snapshot per month (the oldest)</li>
<li>for previous years, keep only one snapshot (the oldest)</li>
</ul>

This is easy to implement because all of my snapshots are named consistently. I've made the script <a href="https://github.com/ngeor/zfs-snapshot-trimmer">available in GitHub</a>.

Hope this helps.
