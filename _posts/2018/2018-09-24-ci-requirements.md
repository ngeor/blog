---
layout: post
title: CI requirements
date: 2018-09-24
published: true
categories:
- tech
tags:
- continuous integration
- quality
- notes
---

There are so many programming languages out there and so many
frameworks to choose from. From a continuous integration
perspective, I think that there a couple of requirements that
one should check before jumping onto something brand new.

## Code style

Having a consistent code style across the codebase makes it
easier to read the code. Having tooling that breaks the build
when the code style is not met allows code reviews to focus
on important things and not blank lines (or the lack thereof).

Such tooling ideally should be present within your favorite IDE,
giving you live feedback as you type. Even better if the tool
offers autofix options, in the IDE, or in batch mode.

In my opinion, it's best to stick with the default style options
and not customize too much. For example, in Java you have
this style for braces:

```java
class MyClass {
    void hello() {
        System.out.println("Hello, world!");
    }
}
```

while in C# you have this:

```cs
class MyClass
{
    void Hello()
    {
        Console.WriteLine("Hello, world!");
    }
}
```

It's best to adopt the conventions (and idioms) of each
programming language (just as you would do when learning a
foreign language). There's nothing preventing you from
writing the Java code in the style of C#, but it would be
extremely weird for anyone else who would try to read it.

In Java there's checkstyle, in C# there's StyleCop. I find
StyleCop's IDE integration quite powerful, but I think it lacks
a command line 'fix all' mode.

I've been teaching myself ruby lately and I use rubocop as a
code style / linter. I have to say that it's the best tool I've
seen in this field. Its defaults are exactly how I like them,
taking into account not only style but also code complexity.
Moreover, it is a **great learning tool**, as it tells you to do
things "the ruby way". Here's a simple example:

```ruby
if !name.empty?
  puts "Hello, #{name}!"
end
```

rubocop tells you that:

- the `if !` can be turned into an `unless`
- ruby has guards

```ruby
puts "Hello, #{name}!" unless name.empty?
```

I want to emphasize that these tools need to break the
build when there are code style violations.

## Documentation

I would like to quote [Google's C++ style guide](https://google.github.io/styleguide/cppguide.html#Comments) (which I
discovered by [AirBnb's Ruby style guide](https://github.com/airbnb/ruby#commenting)):

> Though a pain to write, comments are absolutely vital to keeping our code readable. The following rules describe what you should comment and where. But remember: while comments are very important, the best code is self-documenting. Giving sensible names to types and variables is much better than using obscure names that you must then explain through comments.
>
> When writing your comments, write for your audience: the next contributor who will need to understand your code. Be generous — the next one may be you!

I really appreciate the attention Microsoft
puts in its code documentation and its conventions. For example,
if a comment starts with a verb, then it's always in the third
person in the singular number (i.e. "Gets a value" and not "Get
a value" or "It gets a value"). Boolean getters always must
start with "Gets a value indicating whether".

In my opinion self documenting code and code documentation are
_not_ mutually exclusive. I typically document classes and
public / protected members only. At the same time, I strive
to pick good names for code elements and have short methods
and classes focused on a single purpose. I still need some
comment to tell me the story behind my choices when I look
at the code at a later stage (even my own code).

Verifying the existence of documentation is typically a task
for the code style tool. However, I wanted to highlight it as
a separate point because it's not uncommon for developers
to dislike writing comments. And yes, nobody like this code:

```java
/**
 * Gets the name.
 */
 public String getName() {
     return name;
 }
```

or even worse, the copy-paste comment variation:

```java
/**
 * Gets the name.
 */
 public String getDescription() {
     return description;
 }
```

This is something that your tooling might support. For
instance, checkstyle can be configured to require
comments for methods but not for getters/setters.

## Unit Tests

Now that the code is written in a consistent way and it
is adequately documented, we move to testing. (I'm skipping
over the obvious part that the code needs to compile if
we're talking about a compiled language.) This is more a
question of framework support that it is about the programming
language itself.

My advice is to go with a popular choice within the community
of your stack. For example, .NET users tend to use MSTest.
Angular uses Jasmine in its documentation, which makes it
easier to follow.

The unit test framework will come with its own code to write
assertions. I would recommend exploring a _dedicated_ assertion
library. For instance, there's assertJ for Java and
FluentAssertions for .NET. Their advantage comes from the fact
that they only have one job to do and they do it well.

Ideally, the unit test tooling should produce output in
a format that the CI server can read, so that it can create
nice reports and graphs. The most common format is an XML format
called jUnit or sometimes xUnit.

## Code Coverage

I was surprised that .NET Core did not have a way to measure
code coverage unless you use Windows. Luckily this seems to
have changed recently with the open source coverlet tool.
Ruby did not have branch coverage until the 2.5
version (late 2017).

Code coverage needs to be supported equally at a developer's
machine and at the CI server, ideally with the same tooling. It
should be possible to define thresholds and have the build
break when they aren't met.

## Cyclomatic Complexity

I am only familiar with JaCoCo here. Keeping the cyclomatic
complexity under control is an automated way of ensuring
your code doesn't get inadvertedly infected with poor design.

It would be great if your programming language supports this. I
was pleasantly surprised to see rubocop supports this check.

## Integration Tests

Integration tests is an overloaded term. Without going into
details, these are the expensive tests that use a real
database, perform real network calls, etc. Going one step
further, these are the tests that treat your entire application
as a black box and test it from the outside.

I have a personal favorite here, which is Spring Boot Test
(Java). Spring Boot Test offers a wide range of testing options
that allow you to test your entire application
(`@SpringBootTest` annotation) or just parts of it
(e.g. `@DataJpaTest` for testing only the database layer or
`@WebMvcTest` to focus on the HTTP protocol and controllers).

Launching your entire app (or parts of it) and testing it
should be supported by your stack with minimal effort.

## Wrapping it up

Before choosing a programming language and/or a framework,
be aware that you'll also need the CI tooling to support it.
Do some investigation to avoid unpleasant surprises and make
sure the bar of quality is kept high.
