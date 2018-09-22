---
layout: post
title: How to create a simple web app with maven
date: 2016-09-18 19:37:05.000000000 +02:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags:
- Java
- maven
author: Nikolaos Georgiou
---

This post shows how to create a simple web application with maven. I have the relevant commits as well in GitHub for reference, in case you want to see in more details.

<!--more-->

First, I <a href="https://github.com/ngeor/icqfriends/commit/f7e65dc9ef3bebde3615d204491a26ff181006ed">created an empty project</a> in GitHub, initializing with a gitignore file tailored for Maven projects.

Then, I <a href="https://github.com/ngeor/icqfriends/commit/6a4dfc570496fb20ea3320dd2a820e92d49baadc">generated a sample web app</a> using maven. The command line is rather long:

```
mvn archetype:generate -DgroupId=net.ngeor.icqfriends
    -DartifactId=icqfriends
    -DarchetypeArtifactId=maven-archetype-webapp
    -DinteractiveMode=false
```

The important part if the archetype being used, which is <code>maven-archetype-webapp</code>.

Since, I'm going to use IntelliJ, I <a href="https://github.com/ngeor/icqfriends/commit/2a3b6b8c82fccddf3cc68356c79d404abf5ea8d6">ignored the files IntelliJ places</a> in the working folder. I also made two modifications to the pom.xml: I <a href="https://github.com/ngeor/icqfriends/commit/2b0bca7f46bf69644f9984fe8784ceac87a3896c">defined the Java version to 8</a> and I <a href="https://github.com/ngeor/icqfriends/commit/cd433b32dece27ae4b8df83b96908240b4dec3cf">specified a more recent jUnit version</a> (4.12 is the current latest, but the pom.xml by default uses 3.8.1).

To be able to run the web app from within the IDE and without needing a Tomcat installation to try it, I <a href="https://github.com/ngeor/icqfriends/commit/dcfebe14b71f4f8e9a3f394b55c6613299552d5a">added the tomcat maven plugin to the pom.xml</a>. This is rather handy and it works nice with IntelliJ, being able to run and debug the web app without leaving the IDE.

Finally, I made a small modification to the web.xml: instead of using the old 2.3 DTD schema, I <a href="https://github.com/ngeor/icqfriends/commit/eb6203046077bb842c12044fe698aaa425580269">changed it to a more recent 2.5 XSD</a>.

The reason I went through this little exercise is because I had an old JSP project in NetBeans (not in maven) but I don't use NetBeans anymore. I wanted to see if it's possible to migrate it to maven and run it again to make a trip down the memory lane (the project is at least 10 years old). I think it's best to stick with an IDE-agnostic approach like maven when it comes to organizing your project; and any serious IDE should support maven.

