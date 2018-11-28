---
layout: post
title: Code review guidelines
date: 2018-09-29
published: true
categories:
  - Tech Notes
tags:
  - code review
---

In this post, I'm describing some do's and dont's about code reviews. I'm not
focusing on the technical side, which depends on the technology stack, but on
the process and the etiquette.

First of all, I'd like to suggest this nice blog post: [Code Review Like You
Mean
It](https://haacked.com/archive/2013/10/28/code-review-like-you-mean-it.aspx/)
by [Phil Haack](https://haacked.com/). Lots of great tips in there.

### Author's point of view

#### When to create a PR

Normally, you should create a PR only when you're finished with your ticket
**and** the build is green. If that's not the case, then you will need to
commit additional changes anyway, so why not wait until you're really done?

As an exception to this, you can also create a PR to get early feedback
when you have doubts about how to proceed. Maybe add a note in the title of the
PR such as "WIP" (work in progress) or something better.

#### Size matters

Keep the PR small. Nobody wants to review a huge changeset.

Sometimes a big PR might indeed be inevitable and that's not the end of the
world. However, big PRs usually indicate failure to break down a ticket into
smaller units of work. Think about breaking the PR down to smaller chunks of
work that still add value.

#### Avoid Scope Creep

There's a fine line between the Boy Scout Principle and Scope Creep.

- Boy Scout Principle: leave the code better than you found it.
- Scope Creep: fixing unrelated things (even small things)

The problem with fixing unrelated things is that it might come back to haunt you
in the future. You might be for example trying to understand _why_ a change was
made, but the matching ticket will be pointing to something totally irrelevant.

Example: fixing an easy IE-only bug under a ticket related to SEO.

#### Adding reviewers

Before you can merge a PR, it needs to be approved by at least one person (or
more, depending on your team).

Some people might have more experience with certain parts of the codebase,
so it makes sense to add them as reviewers when that code is being changed.

It might also make sense to wait for these people to sign off the PR, even
though you have already received the necessary approvals by other team members.

#### Be the first reviewer

You can also create a PR without any reviewers, in order to perform first the
review by yourself. Try to put on the code reviewer's hat and see if you've
missed something obvious.

It happens to me more than often that when I do a code review by myself, I find
small things and typos that I can fix before asking for feedback.

#### Annotate in advance

Before appointing the reviewers, you can annotate the PR with guiding comments.
The code reviewer does not have the context of the change on his/her mind. If
you add some comments on what is going on, the code reviewer will spend less
time trying to understand the PR.

Do consider however if these guiding comments would be more useful to live
inside the codebase.

#### Nudging Reviewers

Sometimes it takes a while before you get code reviewers to engage with your PR.
You can use the Nudge button in Slack to gently poke them. You can also mention
it in Slack and perhaps reach out individually.

Patience is a virtue. Wait a bit before poking them.

It is still the author's responsibility to close the ticket, so don't forget to
keep poking at the reviewers.

#### Processing Comments

Even if you have approvals on your PR, make sure that all comments are discussed
and properly addressed before merging a PR. This is more about manners and
etiquette. It is not polite to merge your PR without at least acknowledging the
comments of a reviewer.

You don't have to agree with every single suggestion and process the requested
changes, that's fine. But don't discard a comment without answering it. That's
what the PR is for, to discuss.

### Reviewer's point of view

#### Reacting in a timely manner

Getting a ticket done is a team effort. If you postpone reviews for too long,
tickets pile up and stay in 'code review'.

Context switching is difficult, but before starting something new, consider
going over open pull requests.

#### Avoid the pronoun game

When commenting, try to elaborate a bit. If you use phrases like "move this to a
function" or "it is not needed", the author might not understand what the words
"_this_" or "_it_" are referring to.

#### Don't worry about code style

Don't worry about things like indentation, blank lines, etc.

Code style checks should be part of the build and [the build should break on

code style violations]({{ site.baseurl }}{% post_url
2018/2018-09-24-ci-requirements %}). If that's not the case, then fix that
instead of wasting your energy complaining about blank lines on every PR.

#### Perfect is the enemy of good

- [Perfect is the enemy of good](https://en.wikipedia.org/wiki/Perfect_is_the_enemy_of_good)
- Premature optimization is the root of all evil (Donald Knuth)
- [Software being "Done" is like lawn being "Mowed"](https://twitter.com/ourfounder/status/770075137332932608)

Don't go crazy with requesting too many improvements. If some unfortunate soul
touched a hairy piece of code for a small bugfix, he/she shouldn't have to do
a full refactoring of the entire code base.

If things get out of hand, pause, take a breath, and create a separate ticket.

### Things to check for regardless of programming language

Here's a small list of things you can check for, regardless of the programming
language you're using:

- The PR should not be behind the master branch.
- The PR should be factually correct and not introduce any bugs. It's easy to
  make a typo or have a boolean condition inverted.
- TODOs: don't add todos in the code, because they create a parallel hidden
  backlog of work. If you must include a TODO, link it with a Jira ticket.
- Code and text are in English. No grammar or spelling errors.
- No abbreviations.
- No unused code.
- No commented out code.
- Follow naming conventions.
- The code is tested sufficiently (unit tests, integration tests). Code review
  smell: when a PR has code changes but no matching test changes.
- Add good documentation comments (javadoc, jsdoc, xmldoc) according to the
  linter (at least on classes and public functions)
