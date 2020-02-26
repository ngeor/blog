---
layout: post
title: Deferred LINQ queries in WCF services
date: 2010-09-12 07:21:00.000000000 +02:00
published: true
categories:
- tech
tags: []
---

Consider the following WCF service:

```cs
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.ServiceModel;

namespace WcfService1
{
	[ServiceContract]
	public interface IService1
	{
		[OperationContract]
		IEnumerable<string> GetData();

		[OperationContract]
		CompositeType GetDataUsingDataContract();
	}

	[DataContract]
	public class CompositeType
	{
		[DataMember]
		public IEnumerable<string> Data
		{
			get;
			set;
		}
	}
}
```

as you can see it defines one WCF service with two methods. The first method returns an IEnumerable of strings while the second method returns a class that contains an IEnumerable of strings.

The implementation I have looks like this:

```
using System.Collections.Generic;
using System.Linq;

namespace WcfService1
{
	public class Service1 : IService1
	{
		public IEnumerable<string> GetData()
		{
			List<string> lst = new List<string>();
			lst.Add("hello");
			lst.Add("world");
			lst.Add("!");
			return lst.Where(s => s != "!");
		}

		public CompositeType GetDataUsingDataContract()
		{
			CompositeType composite = new CompositeType();
			composite.Data = GetData();
			return composite;
		}
	}
}
```

The first method populates some sample data on a List and uses a LINQ query to return the data to the client. The second method calls the first method to populate its own results.

You would expect that they both work the same on the client. But they don't. The first method works fine, but the second one throws an obscure CommunicationException with the not so helpful message: <strong>The underlying connection was closed: The connection was closed unexpectedly</strong>. Here's what the WCF client looks like:

```
using System;
using ConsoleApplication1.ServiceReference1;

namespace ConsoleApplication1
{
	class Program
	{
		static void Main(string[] args)
		{
			using (Service1Client service = new Service1Client())
			{
				// this works
				foreach (string s in service.GetData())
				{
					Console.WriteLine(s);
				}

				Console.ReadLine();

				// this does not work
				foreach (string s in service.GetDataUsingDataContract().Data)
				{
					Console.WriteLine(s);
				}

				Console.ReadLine();
			}
		}
	}
}
```

To work around this, you need to force the evaluation of the LINQ query using the .ToArray or .ToList method. Then everything works normally. I'm not sure exactly why the deferred LINQ query works when the list is the direct return value and it fails when it is assigned to a data member of a class that is the returned value...

```
using System.Collections.Generic;
using System.Linq;

namespace WcfService1
{
	public class Service1 : IService1
	{
		public IEnumerable<string> GetData()
		{
			List<string> lst = new List<string>();
			lst.Add("hello");
			lst.Add("world");
			lst.Add("!");
			return lst.Where(s => s != "!");
		}

		public CompositeType GetDataUsingDataContract()
		{
			CompositeType composite = new CompositeType();

			// Fixed by adding .ToArray()
			composite.Data = GetData().ToArray();
			return composite;
		}
	}
}
```
