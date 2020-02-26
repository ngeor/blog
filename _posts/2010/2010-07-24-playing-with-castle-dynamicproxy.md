---
layout: post
title: Playing with Castle DynamicProxy
date: 2010-07-24 21:09:00.000000000 +02:00
published: true
categories:
- tech
tags: []
---

If you've ever used an ORM tool, such as NHibernate or the Entity Framework, you'll probably have noticed that their goal is to be as unobtrusive as possible. They say, and I agree, that you shouldn't be forced to have your business objects inherit from strange classes like MarshalByRefObject, or to annotate your properties with all sorts of ORM specific attributes. In that aspect, I find NHibernate to be rather clean.

But in the end, every ORM tool expects you to call some Save method in order to indicate that at this point you would like the ORM to kick in and do its magic. I was wondering, is it possible to have a piece of code like this:

```
Person person = new Person();
person.Lastname = "Smith";
person.Firstname = "John";
```

and just by using that code to end up with a new record in my database?

Well, technically, it's possible. I played a bit with <a href="http://www.castleproject.org/dynamicproxy/index.html">DynamicProxy</a> to make it work and I enjoyed it. What does DynamicProxy do? It creates dynamic subclasses of your classes at runtime, overriding all virtual members (properties and methods). All calls to those members are intercepted and your interceptors can do additional pre and post processing with those calls. If this reminds you of Aspect Oriented Programming, it's no coincidence. In fact, let's see an example of DynamicProxy in action, using the classic AOP example: Logging all method calls of a class.

So our class Person should look something like:

```
public class Person {
	public virtual string Lastname { get; set; }
	public virtual string Firstname { get; set; }
	public virtual void Print()
	{
		Console.WriteLine(
			"My name is {0} {1}",
			Firstname,
			Lastname);
	}
}
```

Note that all members are virtual so that DynamicProxy will be able to override them and intercept them. We want to print a message to the console everytime a property is being read or written. We'll implement the IInterceptor interface:

```
public class LogInterceptor : IInterceptor
{
	#region IInterceptor Members

	public void Intercept(IInvocation invocation)
	{
		if (invocation.Method.Name.StartsWith("get_"))
		{
			Console.WriteLine("Getting property");
		}
		invocation.Proceed();
		if (invocation.Method.Name.StartsWith("set_"))
		{
			Console.WriteLine("Property set");
		}
	}

	#endregion
}
```

What is happening here? If we access a member of the class that this interceptor is, well, intercepting, the Intercept method is call instead. The invocation argument can provide information about the original call but the most important method is the Proceed, which proceeds with the execution of the original non-intercepted code. The name of the method being called can be found by <code>invocation.Method.Name</code>. Note that properties are actually treated as method calls. The name of the method is the name of the property prefixed with get_ if it's a getter or set_ if it's a setter. In this code, all members are allowed to execute, since the <code>invocation.Proceed()</code> is always called. But if we're getting a property, a message will appear immediately before getting it and if we're setting a property the message will appear immediately after setting it. This doesn't have much value other than demonstrating pre and post processing in an interceptor.

In order to take advantage of the interceptor, we can no longer create our Person objects directly but we have to use DynamicProxy's Proxy Generator. The code for that looks something like this:

```
ProxyGenerator generator = new ProxyGenerator();
IInterceptor logInterceptor = new LogInterceptor();
Person person = generator.CreateClassProxy<Person>(logInterceptor);
```

And that's it! If we now call <code>person.Firstname</code>, instead of our code (which is not much since we're using an automatic property, but ok) what gets executed is the LogInterceptor. In there, a message will be printed notifying us that a property has being accessed and the <code>invocation.Proceed()</code> call allows the execution to proceed normally, returning the property value to the caller as expected.

I had a lot of fun playing with this tool and creating objects that are instantly persisted to the database without requiring an explicit call to a Save method. Of course, this "instant persistancy" technique is a disaster for the database, since every property modification results to a trip to the database. But it was very interesting nonetheless and I hope I'll have a chance to use more of DynamicProxy in the future.
