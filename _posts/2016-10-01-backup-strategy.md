---
layout: post
title: Backup Strategy
date: 2016-10-01 10:16:27.000000000 +02:00
parent_id: '0'
published: true
categories:
- Tech Notes
tags:
- backup
author: Nikolaos Georgiou
---

Taking a backup was arguably easier back in the days. You had only one computer, your data could fit inside a few floppy disks and the only cloud in your life was the one that would indicate chances of rain later in the afternoon. Things are a bit different today. Nevertheless, the need to preserve your files, your work, and your digital memories, remains the same.

<!--more-->

Here's my situation and how I'm trying to backup my documents. First of all, where do my documents live? They're a bit scattered:
<ul>
<li>An old MacBook Pro. The only one that contains large files like photos, music, videos (around 70GB all together).</li>
<li>My server at digital ocean. This is where this blog is hosted. It contains mostly this blog (wordpress installation and database).</li>
<li>A mini Intel NUC computer that is always on. This one has movies and TV series. Arguably it wouldn't be the greatest disaster if I lose those because they're not personal. This is around 1TB of data alone. This computer however has a ZFS raidz1 setup, so it is more tolerant to hard drive failures. I'll come back to that point later.</li>
<li>A samsung laptop (Windows 10). This one doesn't have anything special but I'm contemplating going mac-free, so I'm comparing it against the Mac.</li>
<li>A desktop computer (ubuntu). This has several virtual box images (125GB) of old Windows versions (e.g. Windows 98, Windows 2000, etc). It's the only computer I have that is powerful enough to run virtual machines.</li>
<li>My phone. This has photos that I haven't copied yet to my Mac. I use Google Photos as well, but it's a free account so the Google Photos version is in lower quality.</li>
</ul>

This should be all right? Well, not really. There's the online freebies as well:
<ul>
<li>GitHub. This is very important to me, all my code repositories live here.</li>
<li>Google Drive. I have all sorts of documents in here, going all the way back to my university years. This is synced to my Mac and my Samsung laptop, so there are multiple copies.</li>
<li>Things we don't even think about anymore: email (Gmail), phone contacts (Google Contacts), calendar (Google Calendar), notes (Evernote, started using it last week), todo list (Wunderlist), bookmarks (Google Chrome), maybe more?</li>
</ul>

That's quite a lot actually.

In my backup plan, the mini computer (the always powered on Intel NUC) is the backup center. All information from all sources gets copied there. I dump everything into the ZFS filesystem. Why? So that I have a central location in which everything is stored. If I want to dump everything, and I mean everything, into a big 2-4TB hard drive, I can do that. Also, they get stored in the ZFS filesystem, which means if one of the hard drives there dies, it will continue to operate.

This by the way does not qualify as backup. If I delete a file on the Mac accidentally, I will lose it on the mini as well next time I sync.

So, everything gets dumped into the mini computer and I don't need to do anything about it, it's all automated:
<ul>
<li>I wrote a launchd agent for the Mac (bash script doing rsync) that kicks in automatically</li>
<li>For the Windows laptop a robocopy batch file in the Task Scheduler</li>
<li>The ubuntu desktop has a cron job with rsync as well</li>
<li>I automatically clone all my GitHub repositories with my <a href="https://github.com/ngeor/clone-all">clone-all</a> program</li>
</ul>

On the mini computer itself, I have CrashPlan installed. I recently bought a paid subscription so I can backup to the cloud as well. The initial seeding of the backup is the biggest problem here. To upload 350GB to their servers, it's going to take around 5 months... fingers crossed until then.

I can also take backup to hard drives. I just connect one to the mini computer and I dump everything in there. The plan is to start taking offsite backups as well. Connect a 2TB drive to mini, dump everything, store it outside the apartment somewhere.

In addition to the above, I have TimeMachine on the Mac and FileHistory on the Windows laptop. This makes sense as these are the native backup solutions to Mac and Windows and they're easy to setup. Especially for the Mac, it doesn't hurt to have another backup of the photos for example.

If I want to put this all in a nice diagram, it will look like this:

<img src="{{ site.baseurl }}/assets/2016/backup-strategy-1.png" />

The bold lines are the only ones that qualify as a backup. Google Drive does not count as a backup. If a file gets deleted or corrupted, it's gone. The same for dumping everything to the central mini computer. It doesn't keep history of older copies.

E-mails are one important thing that is missing in this picture. I'm backing them up indirectly, by using Thunderbird as an IMAP client of Google Mail (both on Mac and on Windows). So I do have a physical copy of those e-mails backed up.

I am totally missing contacts, calendar, etc. At this point, these are totally out there in the cloud.

I'm also missing backing up more important files like photos into more media e.g. a memory card or a Blu-Ray disk. And I haven't done any offsite backup yet.

And, most importantly, I haven't tried if I can actually restore a file from the backup. Because, as the old joke says, the backup is 100% successful, it's always the restore that fails.

