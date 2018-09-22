---
layout: post
title: 'Extending NUnit: NUnit Companion'
date: 2012-03-25 14:04:00.000000000 +02:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags:
- NUnit Companion
- pet project
author: Nikolaos Georgiou
---

I have several test fixtures (test classes) written in NUnit that verify my data layer works against a live database (MSSQL). By live I mean that there is no mocking or anything like that - that's for the higher layers where I mock the data layer.

Now, I would like to extend my code to support more databases (MSSQL CE, SQLite) but I don't want to start copy pasting my tests around or to create very complex inheritance strategies. These approaches are time consuming and require significant effort to maintain. Enter NUnit extensibility.<!--more-->

I found most of the information I needed in <a href="http://www.simple-talk.com/dotnet/.net-tools/testing-times-ahead-extending-nunit/">this nice article</a> and I hacked away this morning into a result that works on my machine (TM) - and also on my build server! The source code is available in SourceForge, I wrapped it up in a project called <a href="https://sourceforge.net/projects/nunitcompanion/">NUnit Companion</a>.
<h2>How to use it</h2>

Assuming the old test code looked like this:

```cs
[TestFixture]
public class SelectTest
{
    [TestFixtureSetUp]
    public void TestFixtureSetUp()
    {
        // initialize fixture
    }

    [SetUp]
    public void SetUp()
    {
        // initialize test
    }

    [Test]
    public void CanSelect()
    {
        Assert.IsTrue(5 == 5);
    }
}
```

all I need to have my tests target multiple databases is:
<ul>
<li>Reference the NUnit.Companion.Framework assembly (it has no dependencies)</li>
<li>Replace the TestFixture with MultiTestFixture</li>
<li>Specify the various databases I target as arguments in that MultiTestFixture attribute</li>
<li>Modify the TestFixtureSetUp method to accept a single argument</li>
<li>Use that argument to choose my database</li>
</ul>

```cs
[MultiTestFixture("MSSQL", "MSSQL CE")]
public class SelectTest
{
    [TestFixtureSetUp]
    public void TestFixtureSetUp(string database)
    {
        // initialize fixture
        switch (database)
        {
            case "MSSQL":
                SetupMsSqlDatabase();
                break;
            case "MSSQL CE":
                SetupMsSqlCeDatabase();
                break;
            default:
                throw new NotSupportedException(
                    "Database " + database + " is not supported");
    }

    [SetUp]
    public void SetUp()
    {
        // initialize test
    }

    [Test]
    public void CanSelect()
    {
        Assert.IsTrue(5 == 5);
    }
}
```

That's it! With very little modifications to the test fixture, we enabled it to run twice. None of the Test methods need to be changed at all. The entire test fixture will be run twice. The first time it will run, the test fixture will be setup with the argument "MSSQL" (the argument is passed in the TestFixtureSetUp method). That's when the test will setup whatever it needs to target the MS SQL database. The second time, the test fixture will run again from scratch, this time against MS SQL Compact Edition. The whole set of tests will run twice, no extra effort in code, no inheritance setups, nice and neat. When I want to test against another database, all I need to do is adjust the attribute on the class and the body of the TestFixtureSetUp method.

This is how this type of tests look like in NUnit GUI:

<img src="{{ site.baseurl }}/assets/2012/nunit-companion-example.png" />

Notice how the test fixture has now child test fixtures, each for every database I want to target. The test methods themselves also contain in their name the database, to easily distinguish which database they refer to.

Installation in the NUnit GUI runner is easy. Simply copy the NUnit Companion DLLs to the addins folder of NUnit.
<h2>TeamCity</h2>

Integrating with TeamCity was a bit trickier but it worked in the end. Here's what my configuration looks like:

<img src="{{ site.baseurl }}/assets/2012/nunit-companion-teamcity-configuration.png" />

Some points of interest:
<ul>
<li>The Runner Type is not the familiar NUnit runner but the generic .NET Process runner. Unfortunately the most common NUnit runner doesn't allow specifying additional addins.</li>
<li>The executable we're running is already defined in the build agent's properties and it's the same as the NUnit runner. This time however we need to specify all the parameters ourselves.</li>
<li>Arguments are placed one per line (separating them by space didn't work on my machine).</li>
<li>The arguments are the .NET runtime, the platform, the NUnit version, the NUnit Companion Addin and finally the assemblies to run tests from</li>
</ul>

The user experience doesn't change while watching builds run or observing build results. After all it's the same NUnit runner underneath and it can communicate with TeamCity giving live results. Also code coverage still works as expected.
<h2>References</h2>
<ol>
<li><a href="http://www.simple-talk.com/dotnet/.net-tools/testing-times-ahead-extending-nunit/">Testing Times Ahead: Extending NUnit</a></li>
<li><a href="https://sourceforge.net/projects/nunitcompanion/">NUnit Companion</a></li>
<li><a href="http://confluence.jetbrains.net/display/TCD7/TeamCity+NUnit+Test+Launcher">TeamCity NUnit Test Launcher</a></li>
</ol>
