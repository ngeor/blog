---
layout: post
title: 'Nested classes: Java vs C#'
date: 2013-10-08 19:38:00.000000000 +02:00
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

So I have started reading up on Java. Getting reacquainted with that old friend. Playing with swing components on the UI editor of NetBeans. Reliving the horror of having to declare every exception your method might throw. The ugliness of the XML DOM API. object.setNumber(object.getNumber() + 1) and so on and so on.

But still, it is nice to read up again. I bought a few books. The guilt list of books that I need to reed because I bought them keeps on growing! Currently I'm reading (slowly, my free time is mostly occupied by fitness these days) Core Java Volume I. It's very basic, but I'm resisting and I don't skip through. Even in those basic chapters you can find things that surprise you, that you never really knew, that you forgot, and so on.

I ran into such a thing yesterday, it has to do with nested classes (or inner classes). Both Java and C# support something like this:

```
public class MainClass
{
    private int _value;
    private InnerClass _child;

    public MainClass()
    {
        _child = new InnerClass();
    }

    private class InnerClass
    {
    }
}
```

There's a MainClass that has an InnerClass. In both languages, the inner class has access to all the private fields and methods of the MainClass.

However, in the typical scenario, there is a parent-child relationship between a specific MainClass instance that creates and owns one or more instances of the InnerClass. So, even though InnerClass instances are allowed by the language to access the private members of <em>any</em> MainClass instance, in the typical scenario these instances are really interested in accessing the private members of the <em>particular</em> instance that created them (their parent, their owner object).

In C#, that means I have to write a bit more boilerplate code in order to express that relationship:

```
public class MainClass
{
    private int _value;
    private InnerClass _child;

    public MainClass()
    {
        _child = new InnerClass(this);
    }

    private class InnerClass
    {
        private readonly MainClass _owner;

        public InnerClass(MainClass owner)
        {
            _owner = owner;
        }

        public void PrintValue()
        {
            Console.WriteLine("The private value is {0}.", _owner._value);
        }
    }
}
```

In Java, that parent - child relationship was considered (I suppose) much more important (or common) so it was promoted to a language feature. The inner class instance has an implicit reference to the outer instance. That means I don't need the explicit constructor and whatnot:

```
public class MainClass {
    private int _value;
    private InnerClass _child;

    public MainClass() {
        _child = new InnerClass();
    }

    private class InnerClass {
        public void printValue() {
            System.out.printf("The private value is %dn.", _value);
        }
    }
}
```

That's pretty sweet! I can just reference the private field and it knows it is about the outer <em>instance</em>.

When I read this last night, I started wondering: why have I not been implementing my .NET code like that? Is is possible that .NET supports this and I've been a fool all this time not knowing it? Well, at least as it turned out I wasn't doing it wrong :)
