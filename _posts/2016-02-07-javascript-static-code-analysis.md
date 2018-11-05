---
layout: post
title: JavaScript Static Code Analysis
date: 2016-02-07 07:07:32.000000000 +01:00
published: true
categories:
- Code
tags:
- code review
- continuous integration
- JavaScript
- jscs
- jshint
- maintainability
- readability
- static code analysis
---

Reading code is hard. It's often difficult to understand what the developer was trying to express when he was writing that function. If you keep your old projects around, go ahead and open them. You'll probably struggle to read even your own code. It might even look as if somebody else wrote it.<!--more-->

Reading is hard for many reasons. The difficulty of picking precise names for variables and functions is the first reason that comes to mind. Ill defined architecture, mixing of concerns and bad code in general is another one. But perhaps the most trivial one and the easiest to prevent is <strong>inconsistent coding style</strong>.

Coding style is about whether you use tabs instead of spaces. Whether you place braces on their own line or not. Whether you leave a blank line after the start of the function or not. How many characters can a line be in length. How do you capitalize your code symbols (PascalCase, camelCase, lower_case_with_underscores, etc)? Do you have a different naming convention for constants? For private members?

The list goes on.

Developers and managers alike often fail to understand the importance of consistent coding style. Why should one care how the code looks like as long as it works?

The problem with code is that it is much easier to write than it is to read. And the code is going to be written once, but it is going to be read many times, again and again, trying to solve a bug, refactor a method, add a new feature to an existing class. Having a consistent coding style helps the eyes to skip fast through the code. It's what readability is all about. Perhaps it will take a bit of time for all of the developers to get accustomed to the rules, but that small investment will pay itself back many times over in the future. That's why <strong>it's important that the entire codebase looks like as if it was written by a single person</strong>.

Defining a set of rules is one thing. How do you go about making sure that the rules are respected?

Code reviews is one thing. A developer can read another developer's code before approving it and he can check for these things. However, checking indentation and whitespace consistency is not a fun thing to do. Moreover, it takes a lot of time if you're going to check all these rules manually and you're bound to make a mistake here and there. In the words of Agent Smith, <strong>never send a human to do a machine's job</strong>.

In JavaScript, we can use a tool called <a href="http://jscs.info/" target="_blank">jscs</a> (short for JavaScript code style). This powerful tool takes care of that hassle. It supports many validation rules (over 150) and it defines popular presets that others are already using (like Google) so that you don't have to explicitly define everything. You can pick a preset and fine tune it to your needs.

Consistent coding style and readability is one part of the equation. The other part we can get some help from the machines is checking for <strong>bad practices and subtle code smells</strong>.

JavaScript is a language that, let's put it politely, is not known for its well thought design and consistency. I really like the book "<a href="http://www.amazon.com/JavaScript-Good-Parts-Douglas-Crockford/dp/0596517742" target="_blank">JavaScript - The good parts</a>" and I think somewhere in there the author says "just forget about these parts of the language, use these and you'll be fine". At least that's what I got from that book and it helped me exit the "I hate JavaScript" zone a long time ago.

Even if you're a JavaScript guru (which I'm not), you can always get a bit of help by some linting tool like <a href="http://jshint.com/docs/" target="_blank">jshint</a>. This is going to help you spot nasty issues that can cause bugs. It can detect the usage of undefined variables or functions (hopefully you just did a typo). It can spot unused variables or functions too. Going to best practices, it can warn you about not using triple equals in comparisons. It can prevent you from nesting blocks too deep (sign that you should be creating a separate function).

Both of these tools can be used on the command line directly or with your favorite build system (I currently use grunt). What is really handy is using them real-time inside your editor in a WYSIWYG fashion. Pick an editor that supports these tools, like Atom, it will make your life much easier.

How do you go about using them in your development pipeline depends on the project. Is it a new project or an existing project with a legacy code base?

If it's a <strong>greenfield project</strong>, you have a clean slate. In that case you should configure your CI to break the build on any issue reported by either jscs or jshint. Don't open up the possibility for compromises here. You have the opportunity to maintain a clean code base.

If it's an <strong>existing project</strong>, it depends. jscs comes with an autofix option that can automatically fix most of the trivial issues. Evaluate the code base and see what the damage is. Maybe it's not that bad and you can clean it up easily. Assuming that won't be the case, if your pipeline supports it, you could use jscs and jshint to generate checkstyle reports. Instead of breaking the build, you get back a report that says what your problems are and, most importantly, how many. Again, if your pipeline supports it, you can implement a ratchet system that dictates that the number of problems can only go down. So if you have lets say 600 errors from jscs and jshint combined, 601 will break the build. 600 will not break the build. 599 will not break the build and additionally it will change the threshold for the next build. Note that this might be difficult to implement on some CI servers. If you can't implement it, have at least some manual policy in place that ensures the numbers don't go up and that you get some cleaning up time to fix the mess over time.

A different approach with an existing code base is to add a special ignore comment at the start of every file that has a problem. Both jscs and jshint support this. This is what we tried at work. All files we inherited are this way excluded by the reports and we can break the build on any new errors. Additionally, we have a principle called "<strong>you touch it, you own it</strong>". This means that if you touch one of these ignored files, it's your responsibility to clean it up. Enforcing this principle requires keen eyes during the code review (so it is prone to human error), but so far it has served us well.

I believe I heard this one in a podcast from Scott Hanselman. He was talking about unit tests and how "compilation is your first unit test". To paraphrase that, I would say that <strong>in an interpreted language such as JavaScript, static code analysis is your first unit test</strong>. You wouldn't skip compilation in your C# code, would you?
