---
layout: post
title: Run dotCover from msbuild and ccnet
date: 2012-09-02 07:52:00.000000000 +02:00
published: true
categories:
- Code
tags: []
---

TeamCity is a very nice tool that I use at home. Unfortunately the free license allows up to 20 configurations. That's why I'm experimenting also with another free tool, CruiseControl. It's definitely not as easy as TeamCity, you have to edit (which means learn) an XML file that the server picks up. In general, it probably supports what TeamCity supports, but you have to make everything yourself with a lot of work. Then again, it's completely free.

What I wanted to setup is code coverage. TeamCity offers its own tool out of the box, dotCover. Since that tool is just a command line program, I figured I could reuse it in CruiseControl.<!--more-->
<h2>dotCover</h2>

dotCover is the tool that does the work behind the scenes. In order to invoke it manually, in combination with NUnit, you'll have to run the dotCover executable like this (<strong>all command lines are broken down to multiple lines for readability, should be in a single line</strong>):

```
dotCover analyse
    /TargetExecutable:nunit-console.exe
    /TargetArguments:MyProject.Tests.dll
    /TargetWorkingDir:MyProject.TestsbinDebug
    /Output:report.xml
```

This command will run the tests in the MyProject.Tests.dll with nunit and produce an XML code coverage report in report.xml. The XML report can be useful for generating graphs and statistics (haven't experimented with that yet). It is however possible to generate a much more friendly HTML report by running the command like this:

```
dotCover analyse
    /TargetExecutable:nunit-console.exe
    /TargetArguments:MyProject.Tests.dll
    /TargetWorkingDir:MyProject.TestsbinDebug
    /ReportType:HTML
    /Output:report.html
```

This will generate the report.html file and a folder with CSS and JS that provide a pretty code coverage report.

<img src="{{ site.baseurl }}/assets/2012/dotcover-report.png" />

It is also possible to generate both the XML and HTML reports. To do that, you only need to run the time consuming dotCover coverage part just once. Then, you run dotCover again twice to generate the two reports, telling it to work on the intermediate coverage report file produced on the first run. We'll use that in our build file.
<h2>Environment Variables</h2>

The previous examples of course assume that the dotCover and nunit-console executables are in the same folder or in the PATH. Usually, that's not the case. To make our setup more robust, we'll introduce two environment variables before going any further:
<ul>
<li>DOTCOVER_HOME -> C:TeamCitybuildAgenttoolsdotCover</li>
<li>NUNIT_HOME -> C:Program Files (x86)NUnit 2.5.10binnet-2.0</li>
</ul>

The first path is the path where dotCover.exe resides. The second path is where nunit-console.exe should be found.
<h2>MSBuild</h2>

Now is the time to hack into our csproj file. We could do this directly in CruiseControl's ccnet.config file actually. However, I prefer modifying the csproj file because:
<ul>
<li>the syntax is simpler</li>
<li>I can run it from my development machine as well as from my build server</li>
<li>even if I switch to a different build server, it will work (provided it supports msbuild)</li>
</ul>

We'll use the AfterBuild target. Also, because we typically don't want to run dotCover on every build on our development machine (or maybe you do, your call), we'll only launch dotCover if a certain parameter is passed to msbuild, e.g. RunDotCover=true.

We need to configure the exec task. It accepts a single command line. Because it's likely that our executables (dotCover and nunit-console) are in paths that contain spaces, we need to wrap these paths in quotes. In MSBuild that is actually done in an ugly way, using the <code>"</code> escape:

```
<Exec Command=""$(DOTCOVER_HOME)dotCover"
     /TargetExecutable:"$(NUNIT_HOME)nunit-console.exe"" />
```

Let's define some properties first to keep things a bit neat:

```
<PropertyGroup>
    <DotCoverOutputPath>$(OutputPath)dotCover</DotCoverOutputPath><DotCoverExe>"$(DOTCOVER_HOME)dotCover.exe"</DotCoverExe>
 <NUnitConsoleExe>"$(NUNIT_HOME)nunit-console.exe"</NUnitConsoleExe>
 <DotCoverFilters>+:MyProject*;-:nunit*</DotCoverFilters>
 </PropertyGroup>
```

The properties we just defined are:
<ul>
<li><strong>DotCoverOutputPath</strong>. The path where dotCover will place its reports. That's typically binDebugdotCover. Notice that we're building on top of the existing OutputPath property, so if we're targeting 64bit build the path will adjust itself to binx64DebugdotCover.</li>
<li><strong>DotCoverExe</strong>. This is the full path of the dotCover.exe. Notice how we're using the DOTCOVER_HOME environment variable.</li>
<li><strong>NUnitConsoleExe</strong>. This is the full path of the nunit-console.exe. Again, we're building on top of the environment variable we defined earlier. No need to worry if it's under Program Files or Program Files (x86) or a custom location.</li>
<li><strong>DotCoverFilters</strong>. This is going to be used as the Filters argument to the dotCover call. It has a strange syntax (you can read about it in dotCover's help message) that allows you to include or exclude assemblies and namespaces from the final report. The value specified in the above code block says we want to keep anything that starts with "MyProject" and we want to exclude nunit from the report (by default it gets included too).</li>
</ul>

With these properties, let's see how our AfterBuild target looks like now:

```
<Target Name="AfterBuild" Condition="$(RunDotCover) != ''">
    <Message Text="Running dotCover" />
    <Exec Command="$(DotCoverExe) cover /TargetExecutable:$(NUnitConsoleExe)
        /TargetArguments=$(AssemblyName).dll
        /TargetWorkingDir=$(OutputPath)
        /Output=$(DotCoverOutputPath)$(AssemblyName).cover
        /Filters=$(DotCoverFilters)" />
    <Message Text="Creating XML report" />
    <Exec Command="$(DotCoverExe) report
        /Source:$(DotCoverOutputPath)$(AssemblyName).cover
        /Output:$(DotCoverOutputPath)$(AssemblyName).xml" />
    <Message Text="Creating HTML report" />
    <Exec Command="$(DotCoverExe) report
        /Source:$(DotCoverOutputPath)$(AssemblyName).cover
        /Output:$(DotCoverOutputPath)$(AssemblyName).html
        /ReportType:HTML" />
</Target>
```

We're reusing the AssemblyName property. So if our test project is called MyProject.Tests, we'll end up with a folder binDebugdotCover containing the following:
<ul>
<li>MyProject.Tests.cover - dotCover's code coverage report (the intermediate file needed to generate the text reports)</li>
<li>MyProject.Tests.xml - the XML report</li>
<li>MyProject.Tests.html (and a subfolder with CSS and JS) - the HTML report</li>
</ul>

Notice also that the target will only run if the <strong>RunDotCover</strong> parameter has been set. So by default when you're just building in Visual Studio this target won't get invoked. We'll be passing that parameter through CCNet (short for CruiseControl.NET).
<h2>CCNet</h2>

Let's now have a look at CruiseControl's configuration.
<h3>msbuild task</h3>

We'll need a msbuild task in CCNet:

```
<msbuild>
    <targets>Rebuild</targets>
    <projectFile>$(ProjectName).sln</projectFile>
    <executable>C:WindowsMicrosoft.NETFramework64v4.0.30319MSBuild.exe</executable>
    <buildArgs>/p:BUILD_NUMBER=$[$CCNetLabel] /p:RunDotCover=true</buildArgs>
</msbuild>
```

Note that we're passing the RunDotCover argument to msbuild. The /p: syntax is basically that same as if you would invoke msbuild from the command line. That's all there is to it, if we run the build now in CCNet, it will invoke dotCover and it will generate the code coverage report. <strong>ProjectName</strong> is a variable I have defined to make this block reusable: it's basically the solution name without the sln file name extension. We can do the same for the RunDotCover argument:

```
<msbuild>
    <targets>Rebuild</targets>
    <projectFile>$(ProjectName).sln</projectFile>
    <executable>C:WindowsMicrosoft.NETFramework64v4.0.30319MSBuild.exe</executable>
    <buildArgs>/p:BUILD_NUMBER=$[$CCNetLabel] /p:RunDotCover=$(RunDotCover)</buildArgs>
</msbuild>
```

So we can reuse this block even for projects that don't need dotCover. In that case, we simply won't define the RunDotCover argument in that project's scope.
<h3>Using the XML report</h3>

It's a good idea to include the report of nunit (TestResult.xml) and dotCover's XML into the build log. This way you can write an XSLT file to present the results nicely in the Web Dashboard. You can do that with a merge publisher.

```
<merge>
    <files>
        <!-- nunit report -->
        <file>$(ProjectName).Tests$(binDebug)TestResult.xml</file>
        <!-- dotCover report -->
        <file>$(ProjectName).Tests$(binDebug)dotCover$(ProjectName).Tests.xml</file>
    </files>
</merge>
```

Note that I'm using the ProjectName variable again, assuming that test project is called <code>$(ProjectName).Tests</code>. This is typically the case (e.g. MyProject.Tests) and it shows that if you stick to <strong>naming conventions</strong> you can easily reuse these blocks in ccnet's configuration file.

Another idea for using the XML report is to fail the build if code coverage drops below a certain percentage. Again, I haven't done this, and it will probably need some custom code (a standard TeamCity feature by the way).
<h3>Using the HTML report</h3>

Publish dotCover's HTML report in the artifacts folder and you'll get the nice HTML report available through your web server (assuming you're publishing artifacts through the web server that is):

```
<cb:if expr="'$(RunDotCover)' == 'true'">
    <buildpublisher>
        <sourceDir>$[$CCNetWorkingDirectory]$(ProjectName).Tests$(OutputPath)dotCover</sourceDir>
        <publishDir>$(WorkingMainDir)$(ArtifactsDir)$(ProjectName)dotCover</publishDir>
        <useLabelSubDirectory>true</useLabelSubDirectory>
        <alwaysPublish>false</alwaysPublish>
    </buildpublisher>
</cb:if>
```

What is happening here:
<ul>
<li>We only invoke this publisher when the RunDotCover variable was set to <code>true</code>. This way we make this block reusable even for projects that don't need dotCover.</li>
<li>There's a <code>$(OutputPath)</code> variable that needs to be defined, same as in msbuild. It's also supposed to contain the <code>binDebug</code> path. Keeping the same variable names as msbuild whenever possible is a good idea to avoid confusion.</li>
<li>The <code>publishDir</code> points to the standard artifacts publishing folder, with an extra dotCover subfolder in order to keep reports contained under the same root folder.</li>
<li>The <code>useLabelSubDirectory</code> is set to <code>true</code> so that reports will be divided per build and also we can keep the old reports as a reference.</li>
</ul>

In my case, the final result is that my pretty HTML report is found at:

```
http://myserver/artifacts/MyProject/dotCover/1.0.0.0/MyProject.Tests.html
```

## Conclusion

This took a lot of work to figure out and it helped me learn a few things about msbuild and dotCover. In the end, the extra benefit of tools like ccnet is that you'll have to dive into it and in the process you'll learn about a lot of things that you don't normally need to know. On the other hand, the benefit of tools like TeamCity is that you can accomplish these things with a few clicks of the mouse :)

Hope this helps.
