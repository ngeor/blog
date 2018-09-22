---
layout: post
title: A quickstart Maven archetype for Java 8
date: 2017-02-25 12:08:38.000000000 +01:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags:
- archetype
- Java
- maven
author: Nikolaos Georgiou
---

As a Maven rookie, I often use the quickstart archetype from Maven when I want to create a new Maven project. Unfortunately, that archetype is a bit outdated, which means I have to tweak some details before I can actually use it. I guess I got a bit tired of this and I thought I could create my own archetype that is ready to use.

<!--more-->

In case you aren't familiar with the term, an archetype is another word for a template. It's possible to use an archetype to create a new project and get some boilerplate code and configuration for free. The most basic archetype is arguably <code>maven-archetype-quickstart</code> . This once gives you:
<ul>
<li>a minimal <code>pom.xml</code> file</li>
<li>a java App that prints Hello World</li>
<li>an example unit test file using jUnit</li>
</ul>

This archetype is a bit dated. When I use it, I know that I have to correct a few problems:
<ul>
<li>set the Java version to 1.8 in the pom. Since it doesn't specify a Java version, it defaults to 1.5. That's old. Very old.</li>
<li>upgrade the jUnit dependency from 3.x to the latest, which is now 4.12. This is a major version upgrade, which means that the dummy unit test itself needs to be rewritten in the 4.x style (which is quite shorter by the way)</li>
<li>fix indentation and format the files</li>
<li>finally, a personal pet peeve, because this is who I am: correct the spelling of the word "rigorous". It's spelled "rigourous" in the original sample unit test <code>AppTest.java</code>, and it stings like an eyelash trapped in my eyeball every time I see it.</li>
</ul>

So I thought I could create my own archetype. Turns out it's not very difficult, far from it. I found a <a href="https://maven.apache.org/guides/mini/guide-creating-archetypes.html" target="_blank">guide</a> in the official maven documentation. Eventually I only needed the very last part of the documentation (all the way at the end) which reads "Alternative way to start creating your archetype". Turns out, they have an archetype for creating archetypes:

```
mvn archetype:generate
 -DgroupId=[your project's group id]
 -DartifactId=[your project's artifact id]
 -DarchetypeArtifactId=maven-archetype-archetype
```

Not only that, but the skeleton it creates is based exactly on the archetype I wanted to fix (maven-archetype-quickstart). So this generates the files that I wanted to fix. Easy-peasy. The folder structure is stored in the folder <code>src/main/resources/archetype-resources</code> , containing the files this archetype will generate.

To be able to use the archetype, I have to install it in the local maven repository by running <code>mvn install</code>. In order to use it, it's no different than using any other archetype:

```
mvn archetype:generate -DgroupId=com.mycompany.myapp \
    -DartifactId=myapp \
    -DarchetypeGroupId=ngeor.archetype-quickstart-jdk8 \
    -DarchetypeArtifactId=archetype-quickstart-jdk8 \
    -DarchetypeVersion=1.0.0 \
    -DinteractiveMode=false
```

This is it. The archetype is <a href="https://github.com/ngeor/archetype-quickstart-jdk8" target="_blank">available in github</a> so you can also use it if you like it.

Other things a future version (or a different archetype) could include:
<ul>
<li>add mockito dependency</li>
<li>add a <code>.gitignore</code> file if it is possible</li>
<li>add JaCoCo for code coverage</li>
<li>add a <code>.travis.yml</code> file to enable building with Travis CI (useful for open source projects in GitHub)</li>
<li>add a <code>README.md</code> which already has the markdown code for the Travis badge</li>
</ul>

Hope this helps.

