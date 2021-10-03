---
layout: post
title: 20th Century Code
date: 2016-09-24 13:15:13.000000000 +02:00
published: true
tags:
- notes
---

I spent the previous week migrating some old code I had laying around into GitHub. More specifically, I had a single git repository named "Legacy" that contained all sorts of projects and demos I had created over the years. It's difficult to find exact dates but I found a few that go as back as 1998, so I can justify the title of this blog post.

<!--more-->

Going back to these projects is a trip down the memory lane, often with emotional reactions. The oldest a project, the strongest the nostalgic feeling it brings out. In a way, it's like finding the toys you used to play with as a child.

I thought of putting these things on GitHub, split per project instead of one huge bucket of code. Maybe forming some sort of code museum this way, being able to show what my code used to look like back in the days? I'm not really sure.

I've lost a lot of these code experiments during the years. I remember that in my first computer I was coding in GWBasic and later in QBasic. But I have no single trace of that. I only have Microsoft's <a href="https://en.wikipedia.org/wiki/Gorillas_(video_game)">GORILLA.BAS</a>, <a href="https://en.wikipedia.org/wiki/Nibbles_(video_game)">NIBBLES.BAS</a> and MONEY.BAS. They still work in DOSBox.

Then I discovered Turbo Pascal 6. I also bought a great book for Turbo Pascal 6, which more or less taught me everything I needed to know for many years to come (data structures, algorithms, the book was amazing). I also don't have anything left from that era, except <a href="https://github.com/ngeor/TP6">some small demo programs</a> that probably came later at around 1998-1999.

I can't remember what came next, Visual Basic 6 or Delphi 5. It was the time of Windows 3.11, and then Windows NT, and then Windows 95. <a href="https://www.youtube.com/watch?v=bAv9Y4LB-Fs">Pitfall</a> was the first game for Windows 95, that much I remember. Probably before that, I had also bought a book for Turbo C++ at this point. Turbo Pascal had become Object Pascal, or Borland Pascal, and then Delphi. I have no code whatsoever from Borland C++ which I also played with.

But I do have a lot of Delphi code, which I was even able to migrate last week to Lazarus and they still work. Which brings me to a small subtopic: text encodings. This was an era before UTF-8 and I was still typing Greek in my code. DOS and Windows had different encodings for Greek: DOS used codepage 437 and Windows had its own Windows-1253 character set. And then came also ISO standard ISO-8859-7, almost compatible with Windows but for one character (Ά would swap place with ¶). Boy I'm glad UTF-8 exists today.

Back to Delphi. I salvaged <a href="https://github.com/ngeor?tab=repositories&q=&type=&language=pascal&sort=">a few repositories</a> and moved them to GitHub. Desktop applications, never complete, never fully working. Mostly experiments, to figure out how stuff works. Even using Windows API directly, just to see if it can be done. I kept only the things that I remembered building.

Same for <a href="https://github.com/ngeor?tab=repositories&q=&type=&language=vba&sort=">VB6</a> and <a href="https://github.com/ngeor/vc6">VC++ 6</a>. I only kept a few things. During this migration, I decided to delete the rest. No backup, just delete them. Just like a museum, you don't keep everything. Just a few things that are for one or another reason significant. I remember how much time I spent exploring Windows API (i.e. WM_COMMAND, HWND, LPARAM, this type of things), before I even had internet. I remember how much time I spent trying to figure out how to create a <a href="https://github.com/ngeor/vc6/tree/trunk/ChangeFileTimePS">shell extension</a> for Windows 95.

The closer I came to present day, the more code I could find. Java, JSP. Some Python scripts. I discovered that it was easier to delete these projects, because they didn't give such a strong emotional response. By year 2005, I couldn't even remember if I had really written these things myself.

I also found all sorts of websites I was creating. I did not port these to GitHub as they are a bit more personal. I did not delete them either. It was the time of GeoCities. All sorts of services like that provided free websites, in which they would inject their advertisements. For some reason, I had subscribed to quite a few. I had also placed my HTML digital trace on any web server that my university school permitted me to.

What did I learn from this migration exercise?

Well, first of all I learned that today's browsers don't even bother supporting Java Applets. Chrome doesn't support it, Microsoft Edge the same. I believe I managed to run my <a href="https://github.com/ngeor/java/tree/trunk/apps/jHangMan">hangman game</a> in Safari, but I'm not sure.

Another thing I learned is that exploring all sorts of programming languages is good because you learn more things but it is also bad because you can't be an expert in everything. I have all sorts of code repositories now that I can't even begin to read or understand. It's okay to play with something to learn, but when you're creating something that you'll have to support, stick with one programming language if possible.

Finally, code comments. I was trying to read some of the code I had written 10-20 years ago (yes, 20 years ago!). There were no comments in the code, nowhere. With a notable exception of one C++ file that I had heavily commented. Guess what? I could actually read that file and understand what's going on. In my current role at work, I spend quite some time telling other developers to add comments, unit tests, this type of things. You really have to go through a revelation like that to realize the value of comments in the code. That file with the comments was suddenly as readable as if I had written it yesterday.

If you have a copy of Visual C++ 6 laying around, clone and run my <a href="https://github.com/ngeor/vc6/tree/trunk/BobMarleyTheGod">Bob Marley the God screen saver</a> (1998 or 1999). I still remember the surprise when someone, I think from an Italian magazine, sent me an e-mail asking my permission to include it in their shareware collection CD-ROM. Do you remember the CD-ROM with the shareware collections? They were the best.
