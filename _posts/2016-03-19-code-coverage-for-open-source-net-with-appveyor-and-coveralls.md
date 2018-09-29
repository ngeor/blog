---
layout: post
title: Code coverage for open source .NET with AppVeyor and Coveralls
date: 2016-03-19 09:11:24.000000000 +01:00
parent_id: '0'
published: true
categories:
- Code
tags:
- ".NET"
- AppVeyor
- code coverage
- Coveralls
- mono
- OpenCover
author: Nikolaos Georgiou
---

Code coverage is a useful metric of the quality of your code. It shows how much code is being covered by unit tests. It doesn't necessarily mean that the unit tests are well written, but no metric can probably tell you that. However, aiming for a specific code coverage, let's say 70%, is a good practice, because failing to meet the goal might mean somebody didn't write enough unit tests.

I'd like to have code coverage as part of the CI I had set up in a <a href="{{ site.baseurl }}/2016/03/05/github-badges.html">previous post with Travis</a>. The bad news is that code coverage and Mono seem to be strangers. There is an open source module called monocov but I couldn't get it to work. In fact in the homepage <a href="https://github.com/mono/monocov" target="_blank" rel="noopener">it says it's not maintained</a>. In my opinion, these kind of tools are essential and they should be included in the core Mono package. I hope they change this some day.<!--more-->

Luckily, I found out about <a href="https://www.appveyor.com/" target="_blank" rel="noopener">AppVeyor</a>. AppVeyor is another CI system that is similar to Travis in that it's free for open source projects and it has a good integration with GitHub. It is also configured via a yaml file. The big difference is that AppVeyor uses Windows for the builds, so you're no longer using Mono but .NET. And there, you have better chances with code coverage.

In order to generate the code coverage information, we can use <a href="https://github.com/OpenCover/opencover" target="_blank" rel="noopener">OpenCover</a> as a NuGet package. The following batch file shows installation and usage:

```
nuget install NUnit.Runners -Version 2.6.4 -OutputDirectory tools
nuget install OpenCover -Version 4.6.519 -OutputDirectory tools

.toolsOpenCover.4.6.519toolsOpenCover.Console.exe -target:.toolsNUnit.Runners.2.6.4toolsnunit-console.exe -targetargs:"/nologo /noshadow .GoogleDriveOfflineBackup.TestsbinDebugGoogleDriveOfflineBackup.Tests.dll" -filter:"+[*]* -[*.Tests]*" -register:user
```

In the first two lines we install NUnit and OpenCover in a directory called "tools". Then we run OpenCover. You can read more about the parameters in the <a href="https://github.com/opencover/opencover/wiki/Usage" target="_blank" rel="noopener">usage page of OpenCover</a>. Perhaps it's interesting to note that with the filter parameter we specify that all code is taken into account for the coverage report <strong>except</strong> for code in the *.Tests namespace. You don't want your tests to be part of the report because that will bring the code coverage number up. By definition the test code is always run (covered), so it just inflates the final percentage up artificially if you include it.

The report will be generated in the current folder with the name results.xml. You can use a tool like <a href="https://github.com/danielpalme/ReportGenerator" target="_blank" rel="noopener">ReportGenerator</a> to create an HTML report out of it. But, you can also use <a href="https://coveralls.io/" target="_blank" rel="noopener">Coveralls</a>, another service that is free for open source projects. Coveralls also works fine with GitHub and discovers your projects, just like Travis and AppVeyor do.

For this to work, we need to publish the generated OpenCover report to Coveralls. There's a NuGet package that does exactly that, it's called <a href="https://github.com/csmacnz/coveralls.net" target="_blank" rel="noopener">coveralls.net</a>. Be careful, there are two packages out there with a similar name. The second one is <a href="https://github.com/coveralls-net/coveralls.net" target="_blank" rel="noopener">this one</a> and it doesn't seem to work right. Here's the revised batch file:

```
nuget install NUnit.Runners -Version 2.6.4 -OutputDirectory tools
nuget install OpenCover -Version 4.6.519 -OutputDirectory tools
nuget install coveralls.net -Version 0.412.0 -OutputDirectory tools

.toolsOpenCover.4.6.519toolsOpenCover.Console.exe -target:.toolsNUnit.Runners.2.6.4toolsnunit-console.exe -targetargs:"/nologo /noshadow .GoogleDriveOfflineBackup.TestsbinDebugGoogleDriveOfflineBackup.Tests.dll" -filter:"+[*]* -[*.Tests]*" -register:user

.toolscoveralls.net.0.412toolscsmacnz.Coveralls.exe --opencover -i .results.xml
```

In the last line we run the executable provided by the package, pointing it to the report and telling it it's in OpenCover format.

We're missing one thing: authorizing AppVeyor to publish the results to Coveralls. We'll do that with an environment variable inside appveyor.yml:

```
version: 0.0.{build}
environment:
  COVERALLS_REPO_TOKEN:
    secure: yCIV3arujsrEYPNrM/wQSs1HQThuA8lSzZ9hTcv28fhgYu3aWyPkneGdaIDElJYp
before_build:
  - nuget restore
after_test:
  - cmd: .after_test.cmd
```

Maybe it's worth mentioning that before_build will restore the NuGet packages of the solution. Building and testing is done automagically by AppVeyor so they're not explicitly mentioned here. Code coverage is done by the batch file after_test.cmd and, you guessed it, that is the batch file code listed earlier in this post. In general, I'd like to say that AppVeyor has <a href="https://www.appveyor.com/docs/appveyor-yml" target="_blank" rel="noopener">very good documentation</a> so you won't be lost.

But what I really like here is the support by AppVeyor for encrypting sensitive data, like the coveralls token. Notice that the environment variable COVERALLS_REPO_TOKEN is prefixed by "secure". The actual value is encrypted, so it's safe to store inside GitHub publicly and paste in this blog post.

To encrypt data, you have to go to the menu in AppVeyor and select "Encrypt data":

<img src="{{ site.baseurl }}/assets/2016/encrypt1.png" />

There you'll get a form with which you can encrypt the data. It even gives you the sample YAML code for using it as an environment variable inside appveyor.yml (extra kudos points for usability!).

<img src="{{ site.baseurl }}/assets/2016/encrypt2-1.png" />

You can get the token from Coveralls. It's available on the repository page:

<img src="{{ site.baseurl }}/assets/2016/token.png" />

Coveralls provides something extra that I hadn't seen before: it tells you how much the coverage has changed between each commit and it breaks it down that delta per file too. Nice extra touch.

<img src="{{ site.baseurl }}/assets/2016/coveragediff.png" />

And, of course, both AppVeyor and Coveralls offer pretty badges to add to your GitHub homepage:

<img src="{{ site.baseurl }}/assets/2016/badges.png" />

(The first badge is from Travis, I still have Travis hooked up and it's failing because of their Mono installation)

Note that Coveralls supports all sorts of languages, it's not limited to .NET/C#. I'm looking forward to exploring this on a JavaScript project.

To summarize, the steps to use these tools for your GitHub repository are the following:
<ul>
<li>setup project in AppVeyor. Make sure you get a green build before going any further with coverage.</li>
<li>setup project in Coveralls</li>
<li>authorize AppVeyor to publish to Coveralls via encrypted environment variable</li>
<li>generate OpenCover report. You can also try this one locally before trying in AppVeyor, possibly with the help of ReportGenerator to see that the report is what you expect it to be.</li>
<li>publish report with coveralls.net package</li>
<li>show off your code coverage to the world with badges</li>
</ul>

Hope this helps!
