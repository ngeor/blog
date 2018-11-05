---
layout: post
title: Validate filename conventions with Maven Enforcer plugin
date: 2017-04-17 16:48:54.000000000 +02:00
published: true
categories:
- Code
tags:
- BeanShell
- conventions
- Flyway
- Java
- maven
- maven enforcer
- static code analysis
- yagni
---

In this post I'm using the Maven Enforcer plugin to break the build when certain files don't follow the expected naming convention. It's always a good idea to take the time and implement these checks inside the build pipeline. The alternative is hoping that code reviewers will spot the problems, which is a manual, tedious and error prone approach. Automate all the things!<!--more-->

The use case is that we want our FlyWay database migrations (sql scripts) to be prefixed with a timestamp, in order to avoid collisions when developers work on different tickets that require a database change. You can read more about that topic <a href="http://www.jeremyjarrell.com/using-flyway-db-with-distributed-version-control/" target="_blank">here</a>. The idea is that if two developers are independently changing the database at the same time, they'll both create a migration called v4.sql (for example). The two migrations are completely unrelated so one of them will have a git conflict. If they follow a timestamp filename convention instead, it reduces the chance for such issues (e.g. v20170417181600.sql).

After a bit of googling, I discovered this stackoverflow <a href="http://stackoverflow.com/questions/42341897/how-can-i-check-if-a-filename-in-my-maven-project-contains-certain-characters-a/" target="_blank">question</a> which suggests using the Maven Enforcer plugin. The plugin introduces itself as <a href="http://maven.apache.org/enforcer/maven-enforcer-plugin/" target="_blank">The Loving Iron Fist of Maven</a>, which got me sold already.

The plugin has various <a href="http://maven.apache.org/enforcer/enforcer-rules/index.html" target="_blank">standard rules</a> you can incorporate in your setup. The most extensible one is the <a href="http://maven.apache.org/enforcer/enforcer-rules/evaluateBeanshell.html" target="_blank">evaluateBeanshell</a> rule. It allows you to write custom code inside your pom in a scripting language called <a href="http://www.beanshell.org/" target="_blank">BeanShell</a> (never heard of it, but it is like Java). As long as the code is an expression that evaluates into a boolean, it can consist of any amount of code (<a href="https://www.youtube.com/watch?v=kNS4t5UCBfI">power, unlimited power</a>).

This is how the whole thing looks like (it's inside build/plugins):

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-enforcer-plugin</artifactId>
    <version>1.4.1</version>
    <executions>
        <execution>
            <id>migration-filename-convention</id>
            <goals>
                <goal>enforce</goal>
            </goals>
            <phase>validate</phase>
            <configuration>
                <rules>
                    <evaluateBeanshell>
                        <condition>
                        List filenames = org.codehaus.plexus.util.FileUtils.getFileNames(
                            new File("src"),
                            "**/*.sql",
                            null,
                            false);

                        for (Iterator it = filenames.iterator(); it.hasNext();) {
                            String file = it.next();
                            print("Found SQL file: " + file);
                            passesValidation = java.util.regex.Pattern.matches("^.+[\\/\\\\]V[0-9]{4}([0-1][0-9])([0-3][0-9])[0-9]{6}__BDV.sql$", file);
                            if (passesValidation) {
                                print("Filename passes validation");
                                it.remove();
                            } else {
                                print("Did not pass validation");
                            };
                        };

                        filenames.isEmpty()</condition>
                    </evaluateBeanshell>
                </rules>
                <fail>true</fail>
            </configuration>
        </execution>
    </executions>
</plugin>
```

It configures an execution of this plugin named <code>migration-filename-convention</code>. It runs the <code>enforce</code> goal of the plugin and it hooks into the <code>validate</code> phase of the lifecycle. This means that you can just run <code>mvn validate</code> to run this custom check.

The code of the rule is contained inside the condition element:

```java
List filenames = org.codehaus.plexus.util.FileUtils.getFileNames(
	new File("src"),
	"**/*.sql",
	null,
	false);

for (Iterator it = filenames.iterator(); it.hasNext();) {
	String file = it.next();
	print("Found SQL file: " + file);
	passesValidation = java.util.regex.Pattern.matches("^.+[\\/\\\\]V[0-9]{4}([0-1][0-9])([0-3][0-9])[0-9]{6}__BDV.sql$", file);
	if (passesValidation) {
		print("Filename passes validation");
		it.remove();
	} else {
		print("Did not pass validation");
	};
};

filenames.isEmpty()
```

This is practically Java code with some differences:
<ul>
<li>you don't have to declare the type of the variables (e.g. <code>passesValidation</code> is clearly a boolean)</li>
<li>you can use <code>print</code> for writing text</li>
<li>the most important part: this is supposed to be still a single boolean expression to be evaluated as true or false. That's why you need all the extra semicolons after the <code>for</code> and <code>if</code> statements. Notice that the last line <code>filenames.isEmpty()</code> which is in the end controls if the build passes or not.</li>
</ul>

The logic is simple:
<ul>
<li>Get a list of all SQL files inside the <code>src</code> folder</li>
<li>Iterate over the found files</li>
<li>Test the filename against a regular expression. If it matches, remove it from the list.</li>
<li>This leaves the list containing only invalid filenames. Therefore the build should be green when the list is empty after the for loop.</li>
</ul>

The <code>print</code> statements are useful for seeing what the rule is doing. This is an example of the plugin in action:

```
[INFO]
[INFO] --- maven-enforcer-plugin:1.4.1:enforce (migration-filename-convention) @ inventory-microservice ---
Found SQL file: main\resources\database\V20170803113900__BDV.sql
Filename passes validation
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
```

The other alternative is to implement <a href="http://maven.apache.org/enforcer/enforcer-api/writing-a-custom-rule.html" target="_blank">a full blown custom rule</a> in Java. While that is more structured than adding scripting code inside the pom, it is over-engineering in my mind for what I want. It requires setting up a new project, so that the custom rule can be added as a dependency to the Maven Enforcer plugin's dependencies. That means setting up a git repository, publishing it somewhere in Nexus, having a CI/CD pipeline, the works. You could argue that then you have a custom rule that you can easily share across projects. Or even make a rule that comes with the desired naming convention built-in.

I see many developers who try to make things generic and abstract way too soon. In a lot of these cases, I try to follow <a href="https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it" target="_blank">You ain't gonna need it</a>. In this particular case, I would first implement the naming convention with the beanshell script, as shown in this post. This is enough to solve my actual problem (having consistent filenames). I would only invest in a separate custom rule if the beanshell approach starts to hurt too much for whatever reason.

