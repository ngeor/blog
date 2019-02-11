---
layout: post
title: Keepass - open source without VCS?
date: 2015-12-17 07:30:00.000000000 +01:00
published: true
categories:
- notes
tags: []
---

For reasons that are not important, I have managed to be dependent on two different password managers: <a href="http://keepass.info/">Keepass</a> and <a href="https://www.keepassx.org/">KeepassX</a>. Wanting to get rid of one of them, I started looking around in their websites.<!--more-->

I discovered that Keepass claims to be open source and goes further saying that it is <em>“OSI certified”</em>, whatever that means, since that’s just a logo with no link to anything.

Now, there is in fact a link to download the source code, so technically it is open source. You can download the code as zip file, read it, study it, modify it and so on. However, there is <strong>no public VCS repository</strong>. No git, no svn, no nothing. That is a bit shocking.

According to wikipedia:
<ul>
<li>Keepass was created in 2003</li>
<li>Sourceforge was created in 1999</li>
<li>Subversion (svn) was created in 2000</li>
<li>Git was created in 2005 (that’s 10 years ago)</li>
<li>GitHub was created in 2008</li>
</ul>

I’m mentioning Sourceforge because it seems that Keepass <a href="https://sourceforge.net/projects/keepass/">exists there</a> and even has some <a href="https://sourceforge.net/p/keepass/code/HEAD/tree/">svn repository</a>, which unfortunately doesn’t contain the project’s code and hasn’t been updated since 2009.

I even googled for “keepass source code”, which took me to this <a href="https://sourceforge.net/p/keepass/discussion/329220/thread/b0bb5457/">nice discussion from 2007</a>, where people asked for the repository of the project. My favorite answer is from 2014, where a supporter of this no-vcs approach quotes from the Merriam Webster dictionary to claim that the zip file containing the source code qualifies as a repository…

This is perhaps a testimony to the success of git and GitHub. In 2015, I simply assumed that everybody has already long migrated there. I hope that the Keepass developers will add to their new year resolutions to make their code available online in GitHub.
