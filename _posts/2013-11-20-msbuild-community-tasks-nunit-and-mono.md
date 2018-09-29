---
layout: post
title: MSBuild Community Tasks NUnit and Mono
date: 2013-11-20 21:27:28.000000000 +01:00
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

As an experiment, I modified an NUnit test project to automatically test itself after the build process. This way, the unit tests become an integral part of the build; just by building in Visual Studio you'll know if you've broken a unit test.

I used the NUnit task from the <a href="https://github.com/loresoft/msbuildtasks">MSBuild Community Tasks project</a>. It worked fine on Windows and Visual Studio. Then, I tried to build also in Linux with Mono and as usual there were a few differences. However, it was quite easy to fix.

First of all, file name capitalizations. Linux is case sensitive about filenames so make sure the MSBuild.Community.Tasks.targets file is imported in the csproj file using in the correct case. In my case, I had to change a "Targets" to "targets".

Then, that targets file complained, something about not being able to resolve <code>$([MSBUILD]::Unescape($(MSBuildCommunityTasksPath)</code>. That expression is on the top of the file and it looks a bit complicated for what it is supposed to be doing. Grabbing some inspiration from NuGet.targets, I created two versions of that PropertyGroup: one for Windows, which I left intact because I didn't want to change whatever it's doing, and one new one for "Non-Windows", which I made it look a bit simpler.

So from this:

```xml
<PropertyGroup>
  <MSBuildCommunityTasksPath Condition="'$(MSBuildCommunityTasksPath)' == ''">$(MSBuildExtensionsPath)MSBuildCommunityTasks</MSBuildCommunityTasksPath>
    <MSBuildCommunityTasksLib>$([MSBUILD]::Unescape($(MSBuildCommunityTasksPath)MSBuild.Community.Tasks.dll))</MSBuildCommunityTasksLib>
</PropertyGroup>
```

I went to this:

```xml
<PropertyGroup>
    <MSBuildCommunityTasksPath Condition="'$(MSBuildCommunityTasksPath)' == ''">$(MSBuildExtensionsPath)MSBuildCommunityTasks</MSBuildCommunityTasksPath>
</PropertyGroup>

<PropertyGroup Condition=" '$(OS)' == 'Windows_NT'">
    <MSBuildCommunityTasksLib>$([MSBUILD]::Unescape($(MSBuildCommunityTasksPath)MSBuild.Community.Tasks.dll))</MSBuildCommunityTasksLib>
</PropertyGroup>

<PropertyGroup Condition=" '$(OS)' != 'Windows_NT'">
    <MSBuildCommunityTasksLib>$(MSBuildCommunityTasksPath)MSBuild.Community.Tasks.dll</MSBuildCommunityTasksLib>
</PropertyGroup>
```

The next change is about locating NUnit itself. The NUnit executable will be searched by default somewhere under C:Program Files, which apparently isn't going to work in Linux. Again, with the same approach, we define a property named <code>NUnitToolPath</code> that holds the NUnit path per platform:

```xml
<PropertyGroup Condition=" '$(OS)' == 'Windows_NT'">
    <NUnitToolPath>C:Program FilesNUnit 2.6.2bin</NUnitToolPath>
</PropertyGroup>

<PropertyGroup Condition=" '$(OS)' != 'Windows_NT'">
    <NUnitToolPath>/usr/local/bin</NUnitToolPath>
</PropertyGroup>
```

So for Windows it will look for the executable <code>nunit-console</code> in the first path and for Linux it will use the path <code>/usr/local/bin</code> (that's where my mono installation lives).

One final part has to do with nunit-console itself. In my mono installation, that executable was using the .NET 2.0 version of nunit, which couldn't load my .NET 4.0 unit tests. Since I don't have any .NET 2.0 projects hanging around, I couldn't care less about .NET 2.0 so the solution here was to convert nunit-console into a symbolic link pointing to nunit-console4. Mission accomplished!

What if I had some projects needing .NET 2.0? The <code>nunit-console</code> executable name is hard-coded inside the NUnit task, but MSBuild Community Tasks is open source so I guess one could go about making that value also configurable.

You can have a look at the entire thing at github. Just for the fun of it the other day I started <a href="https://github.com/ngeor/compilers">a project creating a GWBasic compiler in C#</a>. There's a test project over there that shows how to use the NUnit task and there's also the modified version of the MSBuild.Community.Tasks.targets.
