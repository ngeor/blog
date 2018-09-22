---
layout: post
title: On Code Comments
date: 2017-03-10 20:49:08.000000000 +01:00
type: post
parent_id: '0'
published: true
categories:
- Tech Notes
tags:
- comments
- culture
- documentation
- static code analysis
author: Nikolaos Georgiou
---

I recently joined a different team at work, working on a whole different project. For the past one to one and a half year, I did my bit in building up a culture in my old teams regarding code quality and the moral responsibility of a developer towards the codebase (also known as <strong>boy scout principle</strong>). Now, we have to start all over from scratch with the new team.

<!--more-->

One of the first things I asked them to do is to add comments in the code. To keep it fair, we apply a principle we like to call "<strong>you touch it, you own it</strong>". What does that mean? Well, you see, you don't have to go and fix the whole world at once. But, if you add some new code, or if you modify existing code, you have to clean it up so that it lives up to our standards. Our standards can incrementally rise over time, putting the bar of quality higher. But for now, we can at least start defining our standards. For now, let's say that all code needs to be commented. Why do I do that?

In my past experience, I see that developers don't add comments and they have no idea what makes a proper documentation comment. Let's start with the first one. Developers don't add comments. You have various reasons why. They don't see the value, or it slows them down. The more opinionated will say that they favor self documenting code.

I'm 100% in favor of self documenting code. Self documenting code implies that you have chosen the most crystal clear name for your function or class, that clearly conveys the meaning and purpose of your code. As anyone with some experience will tell you, in reality, class names are in the shape of Utils, Helpers, and, oh God, Misc. <strong>Naming things is hard</strong>. It is one of the hardest things in programming. So please don't tell me your code is self documenting. The same applies if your functions are more than 4 lines of code each. Yeah, my code isn't self documenting either, so don't worry too much about it. It's good to strive for self documenting code. But let's be honest about it.

Assuming we haven't reached self documenting code nirvana, let's go back to the difficulty of naming things. Another aspect to this difficulty comes from the fact that most of the team members are non native English speakers. Not everybody has the same fluency in English. Some people may speak well but write poorly and vice versa (or be equally poor in both). These people will struggle the most with picking the correct names for their code elements (or they won't struggle at all and just pick something horrible). What I found in action is that when you force them to write comments, the comment tends to be more descriptive than the code. In other words, the comment contains in one form or another a better name than the name they chose for the function itself. I would often add a code review comment like "great work! Could you please rename your function so that it's closer to what your comment says?". See this example:

```
/**
 * Send an email if the order is shipped.
 */
public void sendEmail(Order order) {
    if (order.isShipped()) {
        Email email = EmailTemplates.build(order);
        email.send();
    }
}
```

Looking at the body of the function gives you an idea of what's going on, but <strong>always think from the caller's point of view</strong> to see if it makes sense:

```
sendEmail(order);
```

Now it seems that we are losing some information. What e-mail is this? Is it always sent? Not so clear now. Perhaps a better name could be <code>sendEmailForShippedOrder</code> but that's a bit too long and overly specific? You could theorize that more of these e-mails will need to be sent, so perhaps rename this function to <code>sendOrderStateEmail</code> ? This might be used in the future to send an email for shipped orders but also cancelled orders? It depends. The point is, the comment was already a bit better than the name of the function (and the real-life examples I've seen where much more striking). By forcing the developer to write the comment, you can potentially help him pick a better name for his class or function.

And yes, nobody likes comments like this:

```
/**
 * Gets the name.
 */
public String getName() {
    return name;
}
```

or even worse, like this:

```
/**
 * Gets the name.
 */
public int getAge() {
    return age;
}
```

They don't add value, or they're plain wrong due to sloppy copy pasting. The only use case for such comments is if you're documenting a library and you intend to publish your documentation too for your library users. Those comments are also code that needs to be maintained, and I'm definitely in favor of less code.

However, I don't want to have to make a judgement call on which code needs to be commented and which doesn't. It's a burden to have the developer come up to you and ask "can I skip the comment here?" or "must I add a unit test there?". It's much easier to have a strict rule "all code needs to be commented". And, that rule needs to be enforced by the CI, otherwise it's again up to the code reviewer to spot it. Break the build on these things. You don't want people checking in code review if all code is properly commented or not. Code review should be for more important things than mechanical checks.

Another thing is that developers don't necessarily know what a <strong>documentation comment</strong> is. Consider the following function:

```
int add(int x, int y) {
    return x + y;
}
```

On their first attempt, a lot of developers will add the following when asked to add comments:

```
// adds two numbers
int add(int x, int y) {
    return x + y;
}
```

A documentation comment is something different. For Java and JavaScript they're a bit similar:

```
/**
 * Adds two numbers.
 * @param x The first number
 * @param y The second number
 * @return The sum of the two parameters
 */
int add(int x, int y) {
    return x + y;
}
```

For C# it looks like this:

```
/// <summary>
/// Adds two numbers.
/// </summary>
/// <param name="x">The first number</param>
/// <param name="y">The second number</param>
/// <returns>The sum of the two parameters</returns>
int Add(int x, int y)
{
    return x + y;
}
```

This particular convention for documenting code can be picked up by tools such as javadoc and generate API documentation that you can publish as web pages. This is exactly how they generate the official documentation for the core libraries of your favorite languages. Additionally, IDEs like IntelliJ and Visual Studio are also tapping into these comments, so you see the documentation of your function when you're trying to invoke it.

After you've gotten the developers to write documentation comments, you'll notice big differences from developer to developer in how they phrase the comments. You can have comments like:
<ul>
<li>"Call this to add two numbers" (talking directly to the programmer)</li>
<li>"Adds two numbers" (answering the question "what does this do?")</li>
<li>"Call me to add two numbers" (the function speaks to the developer)</li>
</ul>

If you notice the core libraries you're already using, they have a very specific and consistent style of documenting code. This needs to apply also to the way we phrase our comments.

Microsoft StyleCop takes the game to the next level and I really like that approach:
<ul>
<li>If a property is read/write, the comment must start with "Gets or sets"</li>
<li>If a property is read only, the comment must start with "Gets"</li>
<li>If a property is write only (not the best idea by the way), the comment must start with "Sets"</li>
</ul>

It has even more specific rules for boolean properties. I'm not going to repeat all three cases, but for a read/write property the comment must start with "Gets or sets a value indicating whether". And you can break the build on these violations if you want.

Once upon a time, I think around 2010, I worked for a year in a project that produced a code library. It was the core engine of a CMS, written in C#. We used StyleCop and that's when I got the habit of writing comments Microsoft style and I learned to appreciate the beauty in that practice.

Opening a file and being able to guess which teammate wrote the code is bad. The team should be writing code in the same consistent style. You should not be able to look at a file and say "oh that's Jim's code" (either with a positive or negative 'oh'). Code comments are also code. Ideally, stylistic options, also on the level of the English being used, should also be taken into account when breaking the build.

