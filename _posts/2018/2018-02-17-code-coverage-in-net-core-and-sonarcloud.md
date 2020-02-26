---
layout: post
title: Code coverage in .NET Core and SonarCloud
date: 2018-02-17 08:39:51.000000000 +01:00
published: true
categories:
- tech
tags:
- ".NET Core"
- badges
- code coverage
- OpenCover
- ReportGenerator
- SonarCloud
---

In this post, I'm creating a code coverage report for a .NET Core project. I'm also using SonarCloud to analyze the project's quality.

<!--more-->

First things first. Code coverage should be something provided for free and out of the box. It should be easy to setup and something that just works. Unfortunately, that's not the case for .NET Core. For the time being, you can only get code coverage either by using Visual Studio Enterprise (which is not free) or by using the open source tool OpenCover (which is Windows only). .NET Core is supposed to be a cross-platform solution and code coverage should also be available cross-platform. I hope this gets addressed in the near future. There is a <a href="https://github.com/Microsoft/vstest/issues/981">GitHub issue</a> which is still open.
<h2>My setup</h2>
<ul>
<li>Windows 10 Home</li>
<li>Visual Studio 2017 Community</li>
<li><a href="https://www.nuget.org/downloads">NuGet</a> on the path</li>
</ul>
<h2>Generating code coverage report</h2>

To generate the code coverage report, I used <a href="https://github.com/OpenCover/opencover">OpenCover</a> and <a href="https://github.com/danielpalme/ReportGenerator">ReportGenerator</a>. The first tool does the heavy lifting of instrumenting the code. The latter generates a friendly HTML report. I have a PowerShell script for generating the report:

```
nuget install OpenCover -Version 4.6.519 -OutputDirectory packages
nuget install ReportGenerator -Version 3.1.2 -OutputDirectory packages

.\packages\OpenCover.4.6.519\tools\OpenCover.Console.exe `
  -oldstyle `
  -output:opencover.xml `
  -register:user `
  -filter:"+[MyApp*]* -[*.UnitTests]*" `
  -target:"C:\Program Files\dotnet\dotnet.exe" `
  -targetargs:"test --no-build MyApp.UnitTests"

.\packages\ReportGenerator.3.1.2\tools\ReportGenerator.exe `
  -reports:opencover.xml `
  -targetdir:coverage
```

Some points about this script:
<ul>
<li>the <code>-target</code> and <code>targetargs</code> parameters specify the command that will run the unit tests. Combined, that's <code>dotnet test --no-build MyApp.UnitTests</code>. The <code>--no-build</code> avoids rebuilding the project, assuming we've already built it.</li>
<li>the <code>-filter</code> argument is used to exclude the unit tests themselves from the coverage report. The unit test code shouldn't be part of the coverage report because then the numbers get inflated.</li>
<li>the <code>-register:user</code> allows this to work without administrator privileges.</li>
<li>the <code>-oldstyle</code> parameter is needed for .NET Core.</li>
<li>the <code>.csproj</code> files need to have full debug information. That's done with the <code>DebugType</code> property.</li>
</ul>

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>netcoreapp2.0</TargetFramework>
    <IsPackable>false</IsPackable>
    <DebugType>Full</DebugType>
  </PropertyGroup>

</Project>
```

OpenCover will generate an XML file at <code>opencover.xml</code> and then ReportGenerator will produce the HTML report at the <code>coverage</code> folder.

<figure><img src="{{ site.baseurl }}/assets/2018/coverage-report.png" /><figcaption>Coverage summary</figcaption></figure>

<figure><img src="{{ site.baseurl }}/assets/2018/coverage-class.png" /><figcaption>Coverage of a class</figcaption></figure>
<h2>Analyzing code quality with SonarCloud</h2>

I discovered the other day that it's possible to use SonarQube online for free for open source projects via a service called <a href="https://about.sonarcloud.io/">SonarCloud</a>.

It's possible to sign in with your GitHub account, as it's expected for this type of tools, like Travis, Coveralls, etc. I've set it up just for the same .NET Core project, as an experiment.

To use SonarCloud, you need to download the <a href="https://docs.sonarqube.org/display/SCAN/Scanning+on+Windows">SonarQube scanner for MSBuild</a>.

The usage involves three steps:
<ul>
<li>starting the scanner</li>
<li>using MSBuild to build the project</li>
<li>stopping the scanner and submitting the analysis to SonarCloud</li>
</ul>

I have a PowerShell script for that:

```
if (-Not ($Env:SONAR_LOGIN)) {
  Write-Error -Category InvalidArgument -Message "Please set the SONAR_LOGIN environment variable"
Exit 1
}

SonarQube.Scanner.MSBuild.exe begin /k:"MyApp" `
  /d:sonar.organization="ngeor-github" `
  /d:sonar.host.url="https://sonarcloud.io" `
  /d:sonar.login="$Env:SONAR_LOGIN" `
  /d:sonar.cs.opencover.reportsPaths="opencover.xml" `
  /d:sonar.coverage.exclusions="**/*Test.cs"

MSBuild.exe /t:Rebuild .\MyApp.sln
.\coverage.ps1

SonarQube.Scanner.MSBuild.exe end /d:sonar.login="$Env:SONAR_LOGIN"
```

Some comments on the script:
<ul>
<li>the <code>SONAR_LOGIN</code> environment variable is my way of committing the script without committing the authorization token. You can get this token from SonarCloud.</li>
<li>you need to use an MSBuild that is compatible with .NET Core. In my case, that's the one that comes with Visual Studio 2017 (found at <code>C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\MSBuild\15.0\Bin</code>).</li>
<li>the SonarQube scanner supports OpenCover, so I'm also running my coverage script here.</li>
</ul>

The first analysis will take more time, subsequent runs are faster. In the end you get a nice dashboard:

<figure><img src="{{ site.baseurl }}/assets/2018/sonarcloud-dashboard.png" /><figcaption>SonarCloud Dashboard</figcaption></figure>

And I see SonarCloud even supports various <a href="{{ site.baseurl }}/2016/03/05/github-badges.html">badges</a> for your README:

<figure>
  <img src="{{ site.baseurl }}/assets/2018/badge-coverage.png" />
  <figcaption>Code coverage badge</figcaption>
</figure>

<figure>
  <img src="{{ site.baseurl }}/assets/2018/badge-quality-gate.png" />
  <figcaption>Quality gate badge</figcaption>
</figure>

<figure>
  <img src="{{ site.baseurl }}/assets/2018/badge-technical-debt.png" />
  <figcaption>Technical debt badge</figcaption>
</figure>
