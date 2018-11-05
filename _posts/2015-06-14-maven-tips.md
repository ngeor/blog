---
layout: post
title: Maven Tips
date: 2015-06-14 07:00:00.000000000 +02:00
published: true
categories:
- Code
tags:
- Java
- maven
---

I started using Maven at work recently. Being a newbie, I find myself googling constantly (even though the answer is always on StackOverflow) about basic things. For reference, these are my most needed actions so far:<!--more-->
<h2 id="how-to-create-a-new-maven-project">How to create a new maven project</h2>

Originally found <a href="http://maven.apache.org/guides/getting-started/maven-in-five-minutes.html">here</a>:

```
mvn archetype:generate \
    -DgroupId=com.mycompany.app \
    -DartifactId=my-app \
    -DarchetypeArtifactId=maven-archetype-quickstart \
    -DinteractiveMode=false
```

Now that’s one long command line…
<h2 id="how-to-define-the-java-version-of-the-project">How to define the Java version of the project</h2>

You’ll need the maven-compiler-plugin. For example, to target Java 1.8, edit the <code>pom.xml</code> like this:

```xml
<project> <!-- root of pom.xml, details deleted for simiplicity -->
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.5.1</version>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                </configuration>
            </plugin>
```

<strong>Update 2018-06-20</strong>: there's a much easier way but I have forgotten to update this post. Just use these properties:

```xml
<properties>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
</properties>
```
 
<h2 id="how-to-specify-the-main-class-of-your-jar-file">How to specify the main class of your jar file</h2>

You’ll need the maven-jar-plugin. Example:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-jar-plugin</artifactId>
    <version>3.0.0</version>
    <configuration>
        <archive>
            <manifest>
                <addClasspath>true</addClasspath>
                <mainClass>com.mycompany.app.Program</mainClass>
            </manifest>
        </archive>
    </configuration>
</plugin>
```

<h2 id="how-to-copy-your-dependencies-to-the-output-folder">How to copy your dependencies to the output folder</h2>

Your jar file ends up being generated to the target folder (don’t forget to add it to the <code>.gitignore</code>!) but the dependencies aren’t copied by default. To do that, you’ll need the maven-dependency-plugin. Example:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-dependency-plugin</artifactId>
    <version>2.10</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>copy-dependencies</goal>
            </goals>
            <configuration>
                <outputDirectory>${project.build.directory}</outputDirectory>
                <includeScope>compile</includeScope>
            </configuration>
        </execution>
    </executions>
</plugin>
```

<h2 id="how-to-copy-extra-resource-files-to-the-output-folder">How to copy extra resource files to the output folder</h2>

This is when you have a few configuration property files in the conf folder and you want to copy them to the same folder where your jar file is going to live. These resource files will not be packaged in your jar file, they will live as standalone files. You’ll need the maven-resources-plugin. Example:

```xml
<plugin>
    <artifactId>maven-resources-plugin</artifactId>
    <executions>
        <execution>
            <id>copy-resources</id>
            <phase>package</phase>
            <goals>
                <goal>copy-resources</goal>
            </goals>
            <configuration>
                <outputDirectory>${project.build.directory}</outputDirectory>
                <resources>
                    <resource>
                        <directory>conf</directory>
                        <filtering>true</filtering>
                    </resource>
                </resources>
            </configuration>
        </execution>
    </executions>
</plugin>
```
