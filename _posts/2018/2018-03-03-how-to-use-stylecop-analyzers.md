---
layout: post
title: How to use StyleCop.Analyzers
date: 2018-03-03 10:14:56.000000000 +01:00
published: true
tags:
- ".NET"
- ".NET Core"
- static code analysis
- StyleCop
- StyleCop.Analyzers
- Visual Studio
---

I played a bit with StyleCop.Analyzers the other day and I wanted to share what I did. I'll be showing how to add a stylecop file, how to use the same rules across projects, how to create a custom ruleset file.

<!--more-->

First of all, I like how easy it is to enable StyleCop with this package. <a href="https://github.com/DotNetAnalyzers/StyleCopAnalyzers">StyleCop.Analyzers</a> is just a NuGet package, so all you have to do is add it to your project. That's all there is to it. As soon as you add it, building the project includes checking it with StyleCop's default rules.

If you're like me, the next step is to be amazed on how many warnings you get by the default rules. So now it's time to configure the tool.

The first thing it complains about is that I should place <code>using</code> directives inside namespace. I prefer that they're outside. It's important perhaps to notice here that the important thing is to achieve a single way of doing things. Whether <code>using</code> statements are inside or outside the namespace is less important; the important thing is that only one way is allowed. Back to the <a href="https://github.com/DotNetAnalyzers/StyleCopAnalyzers/blob/master/documentation/Configuration.md">configuration</a>: we need to create a <code>stylecop.json</code> file in the project:

```
{
  "$schema": "https://raw.githubusercontent.com/DotNetAnalyzers/StyleCopAnalyzers/master/StyleCop.Analyzers/StyleCop.Analyzers/Settings/stylecop.schema.json",
  "settings": {
    "orderingRules": {
      "usingDirectivesPlacement": "outsideNamespace"
    }
  }
}
```

The <code>$schema</code> field adds Intellisense for this json file in Visual Studio. The relevant configuration is in <code>settings.orderingRules.usingDirectivesPlacement</code>.

<strong>Small gotcha</strong>: StyleCop.Analyzers didn't respect my configuration initially. The way it worked was by selecting the file's build action as C# additional file. I don't know if this is the expected behavior but this did the trick for me.

<img src="{% link /assets/2018/03/03/09_48_41-ub-parcelshops-microsoft-visual-studio.png %}" />

That was the first thing I changed. The configuration you can do with the stylecop.json is mentioned <a href="https://github.com/DotNetAnalyzers/StyleCopAnalyzers/blob/master/documentation/Configuration.md">here</a> but I find that it's a bit limited. They do mention that you can use rule set files to fine tune the rules, but the documentation was not very helpful.

So, the next thing I wanted to change is not having to prefix local calls with <code>this.</code>. Suddenly I'd have to prefix every local field, property or method with <code>this.</code>, which I don't really like. This is not possible to configure via <code>stylecop.json</code>, so I need to write a rule set file. I found by luck a much easier way to do that with Visual Studio.

Each of these rules has an identifier, e.g. in this case it was SA1101. I noticed that these rules are available in the Solution Explorer in Visual Studio, by expanding Dependencies, Analyzers, StyleCop.Analyzers:

<img src="{% link /assets/2018/03/03/09_54_54-ub-parcelshops-microsoft-visual-studio.png %}" />

I can right click on the rule that I want and change its severity to None:

<img src="{% link /assets/2018/03/03/09_56_30-ub-parcelshops-microsoft-visual-studio.png %}" />

This will create the ruleset for me in my project! I couldn't find documentation for this feature and I think it should really be part of the StyleCop.Analyzers documentation. The file has an XML format and a ruleset file extension.

The other thing I like with StyleCop.Analyzers is that each rule is documented online and that documentation is available as a link in the build warnings. So when you get a warning, you can simply click on it and go see what the rule is about.

In my case, I disabled three rules overall:
<ul>
<li><a href="https://github.com/DotNetAnalyzers/StyleCopAnalyzers/blob/master/documentation/SA1101.md">SA1101</a> Prefix local calls with <code>this.</code></li>
<li><a href="https://github.com/DotNetAnalyzers/StyleCopAnalyzers/blob/master/documentation/SA1633.md">SA1633</a> A C# code file is missing a standard file header.</li>
<li><a href="https://github.com/DotNetAnalyzers/StyleCopAnalyzers/blob/master/documentation/SA1652.md">SA1652</a> Enable XML documentation output</li>
</ul>

The final part was sharing this configuration with all projects in the same solution. I couldn't find documentation on how to do it, so I improvised. I simply modified all csproj files to reference the files from the first project I added the rules configuration. I had to reference the ruleset inside a <code>PropertyGroup</code> and the stylecop file inside an <code>ItemGroup</code> element:

```
  <PropertyGroup>
    <TargetFramework>netcoreapp2.0</TargetFramework>

  <CodeAnalysisRuleSet>..\FirstProject\FirstProject.ruleset</CodeAnalysisRuleSet>
  </PropertyGroup>

  <ItemGroup>
    <AdditionalFiles Include="..\FirstProject\stylecop.json" />
  </ItemGroup>
```

It would be great if there's a way to package these two files as a NuGet package and reference them in any project that needs to comply to these rules (something that is possible with Maven/Checkstyle and npm/ESLint).
