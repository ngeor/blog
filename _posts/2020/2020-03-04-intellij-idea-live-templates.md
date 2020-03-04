---
layout: post
title: IntelliJ IDEA Live Templates
date: 2020-03-04 09:37:48
tags:
  - IntelliJ IDEA
  - live templates
---

IntelliJ IDEA allows you to save some keyboard strokes by quickly inserting code
that you use frequently. This feature is called live templates (similar to user
snippets in Visual Studio Code).

You can find them in the Settings:

![Live templates](/assets/2020/2020-03-04-live-templates.png)

I have created a new group named "Custom" and inside that group I have three
live templates. As an example, this is a basic template that checks if an
argument is null:

```java
if ($name$ == null) {
    throw new IllegalArgumentException("$name$");
}
```

The `$name$` expression is a variable placeholder.

The abbreviation of this live template is `argnull` so if I start typing
`argnull` in the IDE it appears as a suggestion:

![Live templates typing](/assets/2020/2020-03-04-typing.png)

and by hitting the Tab key, the template expands:

![Live templates expanded](/assets/2020/2020-03-04-expanded.png)

The live templates are stored as XML in the IntelliJ configuration directory, in
my case that is `~/.IdeaIC2019.3/config/templates`.

Another example is defining a logger for a class:

```java
private static final Logger LOGGER = LoggerFactory.getLogger($CLASS_NAME$.class);
```

We can provide an expression for the `CLASS_NAME` variable so that it will be
automatically replaced by the class name of the class where the live template is
expanded into. In our case it's the `className()` function:

![Live templates function](/assets/2020/2020-03-04-function.png)

The documentation lists the available
[predefined functions](https://www.jetbrains.com/help/idea/2019.3/template-variables.html).
