---
layout: post
title: Ubuntu Postfix DNS errors
date: 2013-11-23 06:59:09.000000000 +01:00
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

I've got Postfix setup on my local desktop computer and on my server. On my local desktop, every now and then Postfix stops sending e-mails. The <code>/var/log/syslog</code> gets filled up with DNS related errors:

```
Nov 22 20:24:49 box postfix/smtp[5180]: 09C212FC0859:
to=<email-address>, relay=none, delay=69887,
delays=69887/0.01/0/0, dsn=4.4.3,
status=deferred (Host or domain name not found.
Name service error for name=ngeor.net type=MX:
Host not found, try again)
```

I know there's nothing wrong with my server, because it can pick up e-mails correctly from other sources, so it must be something wrong with Postfix on my local desktop.

Digging around in the usual places (<code>/etc/resolv.conf</code>) didn't help much, after all I didn't experience any other DNS problems using my desktop.

So, <abbr title="Today I learned">TIL</abbr>: Postfix is actually using its own resolv.conf, which can be found in <code>/var/spool/postfix/etc/resolv.conf</code>. And in my case, that file was empty...

I'm not sure what caused the file to become empty, so I'll keep an eye for that.

I did find a script in <code>/etc/resolvconf/update-libc.d/postfix</code> which copies the <code>/etc/resolv.conf</code> over to Postfix's resolv.conf, so I'm assuming that something went wrong there.

Additionally, when running Ubuntu as a desktop, it typically uses its own local caching DNS server, which isn't the case with the server version. So this could also be causing some problems.

For now I just copied over the correct contents from <code>/etc/resolv.conf</code> to Postfix's resolv.conf, which solves the problem (until next time that file somehow gets empty).
