---
layout: post
title: Optional files in Maven archetypes
date: 2019-09-07
published: true
tags:
  - java
  - groovy
  - maven
  - archetype
---

This post shows how to create a Maven archetype that can conditionally include
or exclude files while generating a project.

Strictly speaking, Maven archetypes do not support conditionally including or
excluding content. However, it is possible to run a Groovy script immediately
after the project has been generated. That script can then delete the files that
are not meant to be part of the generated project.

I discovered this by [this answer](https://stackoverflow.com/a/48426833/153258)
on StackOverflow, but the
[official documentation](https://maven.apache.org/archetype/maven-archetype-plugin/advanced-usage.html)
is rather brief and doesn't offer an example. Luckily, searching by the filename
of the script (`archetype-post-generate.groovy`), I found
[a match](https://github.com/liferay/liferay-portal/blob/master/modules/sdk/project-templates/project-templates-rest/src/main/resources/META-INF/archetype-post-generate.groovy).

In my use case, I have a Maven archetype which generates some boilerplate code
to connect to an SFTP server using Spring Integration. I wanted to extend this
to support FTP as well, but Spring Integration for FTP is slightly different
(different artifact, class names, etc). I could try to keep my code in one
class, but I figured it would be riddled with Velocity template conditionals
that would make it difficult to maintain. Instead, I decided to have two
classes, one for SFTP and one for FTP. A property determines which one should be
used, but then I want to keep only one of the two files based on that property.

Here's how the Groovy script looks like:

```groovy
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths

// the path where the project got generated
Path projectPath = Paths.get(request.outputDirectory, request.artifactId)

// the properties available to the archetype
Properties properties = request.properties

// connectionType is either ftp or sftp
String connectionType = properties.get("connectionType")

// the Java package of the generated project, e.g. com.acme
String packageName = properties.get("package")

// convert it into a path, e.g. com/acme
String packagePath = packageName.replace(".", "/")

if (connectionType == "sftp") {
  // delete the FTP file
  Files.deleteIfExists projectPath.resolve("src/main/java/" + packagePath + "/polling/FtpFlowBuilder.java")
} else if (connectionType == "ftp") {
  // delete the SFTP file
  Files.deleteIfExists projectPath.resolve("src/main/java/" + packagePath + "/polling/SftpFlowBuilder.java")
}
```

This script is part of the archetype and needs to live in this location:
`src/main/resources/META-INF/archetype-post-generate.groovy`.
