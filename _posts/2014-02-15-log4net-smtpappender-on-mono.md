---
layout: post
title: log4net SmtpAppender on mono
date: 2014-02-15 08:19:10.000000000 +01:00
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

I have some problems with the SmtpAppender of log4net on mono. I couldn't figure out what was going wrong, it just wasn't sending any e-mails.<!--more-->

With a bit googling, I found a nice trick that lets you <a href="http://mail-archives.apache.org/mod_mbox/logging-log4net-user/200412.mbox/%3C20041218002314.72939.qmail@web40407.mail.yahoo.com%3E">run log4net in 'debug' mode</a>. You have to set the appSetting log4net.Internal.Debug to true:

```
<appSettings>
    <add key="log4net.Internal.Debug" value="true" />
</appSettings>
```

With that, you'll get detailed output of log4net on the console. In there, I found why no e-mails were being set: something about CallContextData not implemented... I guess I've hit on something that isn't implemented on mono? I don't know and I don't care.

All I really want is to receive an e-mail when my app logs an error. That's it. So I put together a small custom appender that does just exactly what I want:

```
public class SmtpAppenderThatWorks : AppenderSkeleton
{
    public string To { get; set; }
    public string From { get; set; }
    public string Subject { get; set; }

    protected override void Append(LoggingEvent e)
    {
        using (SmtpClient client = new SmtpClient())
        {
            using (var msg = new MailMessage(From, To))
            {
                msg.Subject = Subject;
                msg.Body = RenderLoggingEvent(e);
                client.Send(msg);
            }
        }
    }
}
```

Note that the only settings you can set are the e-mail subject and the sender and receiver e-mail addresses. I leave the smtp host and authentication to be handled by the standard <code>system.net</code> configuration section.

No buffering support, nothing fancy, just a small appender that actually works in mono. I used <a href="http://www.codeproject.com/Articles/406634/Creating-a-custom-log4net-appender">this article on CodeProject</a> as a guide to write the appender.

The configuration looks like this:

```
<appender name="SmtpAppender" type="Test.SmtpAppenderThatWorks">
    <layout type="log4net.Layout.PatternLayout">
        <conversionPattern value="%newline%date [%thread] %-5level %logger - %message%newline%newline%newline" />
    </layout>
    <threshold value="ERROR" />

    <to value="recipient@mydomain.com" />
    <from value="noreply@mydomain.com" />
    <subject value="Exception report" />
</appender>
```

