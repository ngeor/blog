---
layout: post
title: Developer Utopia
date: 2017-11-05 11:43:14.000000000 +01:00
parent_id: '0'
published: true
categories:
- Tech Notes
tags:
- governance
- technology radar
author: Nikolaos Georgiou
---

What happens when developers get the full freedom to work on the things they want with the tools they want? "Get the best people, give them the best tools and get out of their way". That <em>should</em> work. The reason it doesn't, it's because we haven't defined what "best" people means.<!--more-->

In this case, a developer is often judged too much on his technical skills. If he knows all these technologies and then more, he should be hired, right? We're not looking enough at people skills. At cultural fit. At his business focus.

Developers can love coding so much that they become one dimensional. They only care for coding. It's important for them, but even more for the business, to realize that they're not hired to code. They're hired to solve the problems of the business. If that problem is solved by code, so be it. Sometimes however, problems are not technical. You need to talk with others. Educate and train. Be patient and show empathy.

What we end up with is what I like to call <strong>hobby developers</strong>, people doing technology for technology's sake. Solving imaginary problems at a scale that the business doesn't require. Randomly onboarding new technologies without any plan. Working on vaguely defined tickets that no product owner asked for. Working on what they think is cool.

And then they quit. They move on to the next adventure. You can see this in job advertisements like "we need a backend developer who knows Perl, C, C#, Java, nodeJS" (they might as well say "we hire anyone with a laptop at this point, save us from this mess!").

Is it the developer's fault? This is moral question. Can you blame a child for eating all the candy when left unattended?

I would be more willing to blame the company. The hiring process should've filtered out such people to begin with. Later on, the scrum team should be mature enough to be business oriented and not solve imaginary problems. That team, through well defined tickets and right prioritization, should've prevented technology for technology's sake from happening. And lastly, management is probably not working out as it should.

I'm not implying that micromanagement is the solution here. Going from one extreme (no management) to the other isn't really going to help much. Technology is an important part of any business and developers have a passion for it. I'm not asking to kill that passion. The question is how to channel that passion in a sustainable way that puts the business problems first.

I think the answer to that is management, governance, processes. Take a look at <a href="https://zalando.github.io/tech-radar/" target="_blank" rel="noopener">Zalando's tech radar</a>, which solves part of the problem I mentioned above. It's a pretty picture, visualizing which technologies are used by Zalando and their level of adoption. Some technologies are adopted, like Java and nodeJS. Some are on trial (Clojure), some are being assessed (gRPC) and some are on hold (.NET languages). I put .NET here on purpose, because I personally really like .NET/C# but, it's on hold, so I can't use it. Period.

Painting a radar obviously is the easiest part. The decision processes behind it are truly the big achievement. You need to have a democratic process, to a certain extent, but also to make sure that decisions are respected and you don't have developers going rogue. Without this governance, you'll have developers picking whatever technology they're familiar with or they want to learn, with little provision for what happens in the long term.

Finally, I want to say how useful it is to see companies publicizing this kind of information. It's a huge advertisement for them of course, because it shows they've got it figured out. But it can also help other companies to set up something of their own. I find it's similar to how companies should publish (some of) their code as open source. They should also publish some of their processes as well.

Because code is only part of the solution.

