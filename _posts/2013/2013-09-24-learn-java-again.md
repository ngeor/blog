---
layout: post
title: Learn Java again
date: 2013-09-24 05:47:00.000000000 +02:00
published: true
tags:
  - notes
  - java
  - C#
---

I've been doing .NET for a long time. I started working on it exactly when .NET
2 was out, so I was lucky to avoid .NET 1 (almost) completely. I love .NET and
C#. I think it's not a coincidence that the
<a href="http://en.wikipedia.org/wiki/Anders_Hejlsberg">main person</a> behind
it is the same person who was behind my favorite products when I was a teenage
coder: Turbo Pascal, Object Pascal and Delphi. There is some sort of
inexpressible similarity, I think, that reflects the designer's choices in the
framework and the language.

There was a time, I still remember, where I was doing Java. I remember doing a
Struts project for an assignment in the university and loving it. Also later,
professionally, a JSP eLearning platform from scratch.

Having spent so much time in .NET, and the Microsoft stack in general, has its
advantages and disadvantages. The obvious advantage is that with .NET and C# I
feel like home. I know it inside out, I know how to get things done. I'm in my
comfort zone.

On the other hand, I'm in my comfort zone. And they say that the interesting
things happen outside that place.

Sometimes I wonder if my learning ability is impaired. Googling for a quick
answer, thinking in 140 characters, "social" network distractions, none of this
existed when I actually learned things.

It's been a very long time since I learned something from scratch. I essentially
taught myself programming. In the beginning it was Basic. GWBasic and QBasic.
With the help of a book that was my introduction to programming and with endless
hours exploring by coding. Those days I didn't have internet. I don't remember
if internet really even existed.

Then came Turbo Pascal. Some guy at the local computer shop had suggested to
give it a try. I bought a book there and I dove into Turbo Pascal 6.
Coincidentally the book was also covering some topics about data structures such
as linked lists and algorithms such as quick sort. That was a very lucky
coincidence.

Then I explored Turbo C, but I guess I liked Turbo Pascal's syntax better. Then
came Borland Pascal (or was it called Object Pascal?) and then the magnificent
Borland Delphi (anyone remembers the <a href="http://delphi.icm.edu.pl/">Delphi
Super Page</a>?).

Around the same time I got a copy of Visual Studio 6. Visual Basic, probably the
easiest of all but also Visual C++ and programming using Windows API. Again,
without internet, just by diving into the help files and examining the functions
of Windows API, the WPARAMs, LPARAMs, etc. That was fun times.

I'm doing a kind of long trip down the memory lane and I'm not sure if I'm
remembering everything right, but I guess Java came after all that. I think I
must've seen Java in the university for the first time. The promise that you can
write it once and run it anywhere was really enticing. I was also exploring
Linux at that time as an alternative to Windows and open source in general as a
philosophy. Plus, Java was another cool thing to learn.

During my time in the university I was always looking for a job on the side. I
wasn't challenged by most of the computer science related courses in the
university and I had the time to spare. I was coding anyway as a hobby for my
pleasure (another thing I haven't done in a long time), why not get paid for it?
I did a VB6 project, a JSP project and then I found a more permanent job that
landed me on the Microsoft stack. Starting with classic ASP and all the way up
to .NET 4, I worked with a small team of highly skilled professionals and we
delivered amazing work.

I also did a Java project in parallel (part-time) somewhere back then
(2005-2006)... but that was a long time ago. I haven't had any serious Java
hands-on experience since 2007 (with a small exception of a month around late
2009).

So, I want to see if I can re-learn Java. First of all, I want to get my ass
down and learn something again. From scratch. Like in the old days. Just to see
if my brain still works. Hopefully with the help of a book, instead of
programming my Googling. It should be possible that I can still remember how to
read a book:

One thing that depresses me about .NET is that it's tied to the Microsoft stack.
Yes, I know, there is Mono. I have spent endless days trying to make sure my pet
projects run also on Mono. The pain is infinite. Also, after Novell fired the
Mono team, my general feeling is that Xamarin's priority is to make ends meet,
so they're focusing on what brings the bacon on the table (nothing wrong with
that) instead of let's say supporting the latest and greatest of ASP.NET. I
don't want to say too much, because it might sound too negative, and Mono is not
my point here. I think the overall accomplishment of Mono is amazing. But it
doesn't come close to delivering the promise "write once, run anywhere".

So I still do some home programming from time to time. Sometimes this turns into
a pet project. Sometimes the pet project evolves into a web app and goes live.
If people use it, you can't really take it down, can you? I would like to be
able to host these pet projects on a Linux virtual machine. So far, I'm stuck
with a Windows VM. I also prefer Windows over Linux for desktop usage, but when
it comes to server administration I really find myself very comfortable with a
terminal and bash. This very blog is hosted from a PC in my house. I like doing
all the web hosting administration, backup, etc. I do the same with my Git
repositories. I find all that administration and, most importantly, automation
easier in Linux.

It's not an easy decision to give up completely something that you love (that's
.NET) and that you've invested so much time into. So I'm not saying that I am
going to. Isn't it funny how much emotion can exist in a decision about cold
technology? It's like my favorite toy. Can you give up your favorite toy and
start playing with something else after all this time?

So for now I think I'll get started on seeing what's around. NetBeans had always
been my favorite over the dreadful Eclipse (I hope this war is still relevant).
I noticed that for the web they still have struts but there other kids on the
block too, JavaServer Faces and Spring MVC.

I was also browsing the Oracle (I miss Sun already) site regarding
certifications. Maybe that could a goal for this learning adventure. Not only
get reacquainted with an old friend but also get a certification about it. The
thing is, there was a sample question in there regarding the order of some
statements. It had a static constructor, a normal constructor and one thing that
I don't remember anymore what kind of constructor it is. I got it wrong because
I didn't notice that last one I guess, but there was a time when I knew these
things.

So what do I want to learn, besides the language? Well, a web framework or two.
How to do REST services and clients. Pick up Hibernate (I use NHibernate on my
pet project). See the administration side of things, application deployment,
build server, unit testing and all these things that I take for granted in .NET.
How to make the equivalent of a Windows service, long running tasks,
asynchronous programming...

Perhaps a nice challenge would be to break down my current .NET pet project into
parts that I could gradually migrate to Java parts... for example, there's some
logic that fetches a web page, applies a regex and returns some data. Currently
that's just a method call but it could be changed into a webservice call and
then that webservice could be re-implemented in Java.

Final question, since this is a long post already. Why Java? Well, it is an old
toy of mine. I want to play with it again. It might bring my home server
situation to a more homogenous (read: no Windows as server) state. I think it's
also a valued skill in the market.

Why not something like Ruby? Well, maybe next time... why not Python? Why not
Go? Why not... the list could be endless but I think that these are not as
mature as Java and while I want to learn, I don't want to be investigating
issues like "my mysql gem doesn't compile because I'm missing some weird
dependency"...

I guess it's studying time! Time to find a book...
