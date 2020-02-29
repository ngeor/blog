---
layout: post
title: How to fail your project
date: 2010-08-10 18:33:00.000000000 +02:00
published: true
tags:
- notes
---

The following list presents a few ways to screw up a project. Please use it only to save your project and not otherwise. Using this list for intentionally screwing up a project is forbidden.

<strong>Don't write documentation</strong>. Why spend time writing down stuff that nobody reads anyway? Instead use face to face conversations where everyone leaves happy with their own conclusions. Make sure that you don't include in these conversations other people that might benefit from them. The best thing to do is keep them out of the loop and let them continue with their work. Don't communicate the results of these conversations with e-mail or any other tangible means; this can lead to proof and proof can lead to documentation. If you do send an e-mail, follow the same rule and don't send it to anyone who might actually gain knowledge from it or provide additional or different information. Every bit of knowledge must be kept in a "he said she said" level, so that nobody can be held responsible about anything.

<strong>Don't respect the coding guidelines</strong>. Code is poetry, poetry is art and art should be free. Don't listen to the lead developer who insists on maintaining a coding style. Live for today and forget about tomorrow. All these warnings that ReSharper (or anyother tool) display are for informational purposes only. If the compiler can read it, then the other developers can read it too. Extra bonus if you type in documentation in broken English that only you can understand.

<strong>Don't write unit tests</strong>. You know that it works. You tested it from the GUI. Once. Well, sort of. Anyway, it doesn't matter. If the other developers find out that it doesn't work, they probably are the ones who broke it. Claim that "it worked on my machine" and "I don't know what happened". It's a slim chance that they will be able to present evidence that they didn't break. If the others feel unit tests are important, they can write them themselves. You've got better things to do, like, write the actual code. You're saving the project while the others are slacking off writing unit tests. They should give you a medal!

<strong>Don't communicate with the others</strong>. If you do something that will affect others, don't tell them. If they are smart they will figure it out themselves. Why distract them anyway? They're busy. And it's a minor change anyway, right?

<strong>Don't ask for help</strong>. This is a special case of the previous one. If you are not sure about something, don't ask for help. Instead, assume how it should work and just write some code. Ideally, sneak-in the code and don't have it reviewed by another team member. This ensures that other people will consider it a fact. Think of all the endless meetings you just saved your team.

Bonus for international teams: <strong>Don't speak English</strong> (or whatever language that the entire team happens to speak). Effective communication is only done by speaking in your native language. If you are the most knowledgeable person in the team, this ensures that your job safety is guaranteed, at least until your company goes bankrupt, for some other unrelated reason of course. If on the other hand you're the person who knows the least, you can continue to work happily while the others discuss in their own language about how the feature you've been working on for the past week should be dropped altogether.

If the developers in your team are doing one or more of the above, your project will probably fail in some way. If the developers in your team are doing all of the above, you can rest asured that your project will fail so bad that people will actually discuss about it in the years to come and even refer to it as "that failed project".

<strong>Final tip for managers</strong>: If you are a manager in such a project, don't make the mistake of firing the person or persons who have repeatedly practiced the above examples, especially if you're the one who hired him. That will make you look bad for hiring an incompetent developer in the first place. Instead, let the mess continue, with the sane developers sinking further more in despair. This way, all the developers will look bad, but you won't, ensuring that your bonus is not harmed in any way.
