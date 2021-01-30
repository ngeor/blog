---
layout: post
title: How to create a simple web app with maven
date: 2016-09-18 19:37:05.000000000 +02:00
published: true
tags:
- java
- maven
---

This post shows how to create a simple web application with maven.

<!--more-->

First, I created an empty project in GitHub, initializing with a gitignore file tailored for Maven projects.

Then, I generated a sample web app using maven. The command line is rather long:

```
mvn archetype:generate -DgroupId=net.ngeor.icqfriends
    -DartifactId=icqfriends
    -DarchetypeArtifactId=maven-archetype-webapp
    -DinteractiveMode=false
```

The important part if the archetype being used, which is <code>maven-archetype-webapp</code>.

Since, I'm going to use IntelliJ, I ignored the files IntelliJ places in the working folder. I also made two modifications to the pom.xml: I defined the Java version to 8 and I specified a more recent jUnit version (4.12 is the current latest, but the pom.xml by default uses 3.8.1).

To be able to run the web app from within the IDE and without needing a Tomcat installation to try it, I added the tomcat maven plugin to the pom.xml. This is rather handy and it works nice with IntelliJ, being able to run and debug the web app without leaving the IDE.

Finally, I made a small modification to the web.xml: instead of using the old 2.3 DTD schema, I changed it to a more recent 2.5 XSD.

The reason I went through this little exercise is because I had an old JSP project in NetBeans (not in maven) but I don't use NetBeans anymore. I wanted to see if it's possible to migrate it to maven and run it again to make a trip down the memory lane (the project is at least 10 years old). I think it's best to stick with an IDE-agnostic approach like maven when it comes to organizing your project; and any serious IDE should support maven.
