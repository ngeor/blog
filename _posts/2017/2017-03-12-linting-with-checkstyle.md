---
layout: post
title: Linting with Checkstyle
date: 2017-03-12 18:15:26.000000000 +01:00
published: true
tags:
- Checkstyle
- IntelliJ IDEA
- java
- maven
- SonarQube
- static code analysis
- TeamCity
---

Code is going to be written once but read many times. A consistent coding style across the entire code base is important to increase readability and maintainability. Luckily, there are tools that can help to define and enforce such styling rules. From mere cosmetics up to nasty code smells, static code analysis can help increase the quality of your code. I wrote some posts on <a href="{{ site.baseurl }}/2016/02/07/javascript-static-code-analysis.html">static code analysis in JavaScript</a> a bit more than a year ago (which in the JavaScript world means the tools are now different, ESLint instead of JSCS/JSHint). In this post we'll see the Checkstyle tool in the Java world, how to use it with TeamCity and IntelliJ and finally a few words about SonarQube.

<!--more-->

Checkstyle is easy to integrate in your existing Maven project. You can add it to your pom:

```xml
<project>

    <properties>
        <maven.checkstyle.plugin.version>2.17</maven.checkstyle.plugin.version>
    </properties>

    <reporting>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-checkstyle-plugin</artifactId>
                <version>${maven.checkstyle.plugin.version}</version>
            </plugin>
        </plugins>
    </reporting>

</project>
```

This configures it as a reporting plugin. You can then run <code>mvn checkstyle:checkstyle</code>, which will generate a report, listing the violations that are found.

Note that you can additionally configure it as a build plugin and use it to break the build with <code>mvn checkstyle:check</code>. This one will break the build if you have any violations whatsoever. You can also configure the plugin so that the check is done automatically during the default lifecycle. This might not be a good idea for an existing project that has too many problems to solve.

As I mentioned in the <a href="{{ site.baseurl }}/2017/03/12/code-coverage-with-jacoco.html">previous post about JaCoCo</a>, <strong>TeamCity can really help solving the problems one step at a time</strong>. It supports consuming the XML report that Checkstyle generates and understands it as Inspection Errors. This is a built-in metric of TeamCity, which means that you can define a custom failure condition for that metric. It's a two step configuration process. First, you need to tell TeamCity where to find the report. That's done with the XML report processing Build Feature:

<img src="{{ site.baseurl }}/assets/2017/teamcity-checkstyle.png" />

Just like with code coverage, you can tell TeamCity to break the build if you have more Inspection Errors than the last successful build. This ensures <strong>we can only improve the code, we can't make it any worse</strong>.

<img src="{{ site.baseurl }}/assets/2017/teamcity-inspection-errors.png" />

I don't know if it gets better than this, but this is pretty neat.

Back to Checkstyle itself, perhaps it's a good idea to see what is it offering us actually. We haven't specified any rules, so by default it uses the <strong>Sun rules</strong>. If you're too young to remember, Java used to belong to a company called Sun Microsystems (if you think this is funny, go talk to a 20-something colleague about Sun). The rules are defined and configured in an XML file and you can <a href="https://github.com/checkstyle/checkstyle/blob/master/src/main/resources/sun_checks.xml" target="_blank">see it in the Checkstyle repository</a>. My advice is to use this as a base and start building your own rules. There are <a href="http://checkstyle.sourceforge.net/checks.html" target="_blank">a lot of rules</a> that you can use and the default set doesn't use a lot of them. If you're like me, you'll feel like a kid in a candy store. Even better, because linting has no sugar! But let's see how to customize your rules.

To <strong>define your own rules</strong>, start by downloading the Sun XML file in order to use it as a base. Put it in your code repository, call it something like checkstyle.xml or my-company-checkstyle.xml, your pick. You now have to configure the pom to use this file instead of the default. As per the documentation, you just need to add this bit in the reporting plugin configuration:

```xml
<configuration>
    <configLocation>checkstyle.xml</configLocation>
</configuration>
```

I made some rules more relaxed and I added some rules that were missing and I find useful. First, the rules I relaxed:
<ul>
<li>disabled the <strong>JavadocPackage</strong> rule. Since I'm not writing library code, I think that documenting packages are a bit too much for me.</li>
<li>changed the <strong>JavadocVariable</strong> rule to be a bit more lenient. I don't want to document private fields, because usually the documentation will be on their corresponding getter/setter method. I do want to document protected/public fields, because if they exist, they are probably important. Ideally fields should be private, so a protected/public field better have a good documentation comment to justify it.</li>
<li>relaxed a bit the <strong>AvoidStarImport</strong> rule. By default it doesn't allow you to do things like <code>import java.io.*</code>. However, I like to let IntelliJ do these things automatically. If IntelliJ wants to use star imports, I'm fine. I allowed a few packages to ignore this rule such as <code>java.io</code>, <code>java.util</code></li>
<li><strong>LineLength</strong> limits lines to 80 characters which is a bit retro (80x24 anyone?). I set it to 100 characters.</li>
<li>The <strong>HiddenField</strong> rule tells you when a method parameter is hiding a class field of the same name. Well, I actually do that on purpose for setters and constructors. Luckily the rule acknowledges these cases and offers to ignore them.</li>
<li>Disabled the <strong>DesignForExtension</strong> rule. It confused me a bit. It said either add a javadoc comment to the method that explains how to override it or make it final. I am already demanding comments, so I find this rule a bit pointless. It is probably more suited for library code, but still, I don't understand the value of it, since adding a comment makes it happy.</li>
<li>Disabled the <strong>FinalParameters</strong> rule. This one demands that the parameters of every method are declared as final. I find that a bit too much typing and there is a different rule that I enabled (ParameterAssignment) that accomplishes the same end goal, which is don't allow re-assignment of parameters.</li>
</ul>

And now, the rules I added. They're quite a lot but you're probably already using them without enforcing them:
<ul>
<li><strong>CovariantEquals</strong>: this one tells you to implement <code>equals(Object)</code> if you already implemented <code>equals(MyType)</code>.</li>
<li><strong>DeclarationOrder</strong>. This one tells you how to order things in a class. First the static fields, then the instance fields, then the constructors and then the methods.</li>
<li><strong>DefaultComesLast</strong>. This one makes sure the <code>default</code> label in a switch statement is the last one. I haven't seen anyone breaking this rule but you never know.</li>
<li><strong>EqualsAvoidNull</strong>. This is a nice one, I actually practice this. Basically, prefer <code>"hello".equals(variable)</code> instead of <code>variable.equals("hello")</code> because it is guaranteed the <code>"hello"</code> literal is not null.</li>
<li><strong>ExplicitInitialization</strong>. I like the rationale they provide for this one. If you're explicitly initializing a field with the default value of its type, you're not confident enough in your knowledge of how it works.</li>
<li><strong>FallThrough</strong>. Prevents falling through multiple cases in a switch statement.</li>
<li><strong>IllegalCatch</strong>. It will break if you're trying to catch an unchecked exception or the <code>Exception</code> exception itself.</li>
<li><strong>IllegalThrows</strong>. Similar to the previous one, prevents you from throwing an <code>Error</code> or a <code>RuntimeException</code>.</li>
<li><strong>IllegalTokenText</strong>. I like this one because I used something similar in JavaScript. It will break if your literals contain some text they shouldn't contain.</li>
<li><strong>IllegalType</strong>. This one allows you to prevent certain types from being used as variables, return types or parameters. The rationale is to not have coupled code to specific classes when there are interfaces. By default, it will complain for HashMap (use Map), HashSet (use Set), etc. Obviously you can still instantiate these types, but the variable you assign them to must be of the matching interface type.</li>
<li><strong>ModifiedControlVariable</strong>. Prevents you from modifying the for loop variable inside a for loop.</li>
<li><strong>MultipleStringLiterals</strong>. If a string literal is repeating in a file, why don't you make a constant out of it?</li>
<li><strong>MultipleVariableDeclarations</strong>. Makes sure each variable is declared on its own line and with a separate statement.</li>
<li><strong>NestedForDepth</strong>. Prevents deep nesting of for loops.</li>
<li><strong>NestedIfDepth</strong>. Prevents deep nesting of if statements.</li>
<li><strong>NestedTryDepth</strong>. Prevents deep nesting of try-catch-finally blocks.</li>
<li><strong>NoClone</strong>. A bit opinionated, it tells you to not use the <code>clone</code> method in order to implement cloning. It cites <a href="https://www.amazon.com/Effective-Java-2nd-Joshua-Bloch/dp/0321356683" target="_blank">Effective Java: Programming Language Guide First Edition by Joshua Bloch</a> as a reference, which pretty much got me sold instantly.</li>
<li><strong>NoFinalizer</strong>. Checks you're not using finalizers.</li>
<li><strong>OneStatementPerLine</strong>. Well, it makes sure each statement is placed on a separate line.</li>
<li><strong>OverloadMethodDeclarationOrder</strong>. Checks that overload methods are grouped together.</li>
<li><strong>PackageDeclaration</strong>. Makes sure classes are not defined in the default package.</li>
<li><strong>ParameterAssignment</strong>. Method parameters should not be modified within a method. Instead, define a new variable that says what you're trying to do.</li>
<li><strong>ReturnCount</strong>. Multiple return statements can be confusing because they create multiple exit paths in a method. This rule defines a maximum.</li>
<li><strong>StringLiteralEquality</strong>. Makes sure you are not using the <code>==</code> or <code>!=</code> operators to compare strings. This can be a life saver if your background is non-Java.</li>
<li><strong>UnnecessaryParentheses</strong>. Complains if you put unnecessary parentheses in expressions.</li>
<li><strong>CommentsIndentation</strong>. Makes sure comments are indented properly.</li>
<li><strong>EmptyLinesSeparator</strong>. This governs the empty lines between code elements. I configure it so it's not mandatory to add an empty line between fields, it is mandatory to have an empty line between other elements and it's not allowed to have multiple empty lines. Heaven.</li>
</ul>

One final step remains: use <strong>Checkstyle in the IDE</strong>. I use IntelliJ these days and it happens that there's a plugin for Checkstyle. It's called Checkstyle-IDEA and its configuration looks like this:

<img src="{{ site.baseurl }}/assets/2017/checkstyle-idea.png" />

Some interesting points:
<ul>
<li>You have to point it to your custom rules if you have these, otherwise it uses Sun's rules as well</li>
<li>By default it will list violations as errors (red color), which can be a bit annoying for a legacy project. You can  tone it down to list them as warnings and leave the error highlighting for the actual compilation errors.</li>
<li>Scan scope intrigued me because by default it won't check your test code. I don't understand why and I don't know what the default behavior of the checkstyle tool is. I will have to look into that at some point. In my mind, test code is also code, it should adhere to the same standards.</li>
</ul>

Once you install the plugin and configure it, you're good to go. You will see the Checkstyle violations as you type, in the usual fashion of IntelliJ.

One final comment about <strong>SonarQube</strong> and why I don't like it. SonarQube is a code analysis service. It analyzes your code and gives back a report about its quality. Some of its features overlap with code coverage and static code analysis, but I think it offers some more. It classifies the problems by severity and gives you an estimate of how much time it will take to resolve these issues (e.g. "you have 5 months of technical debt").

Here's some reasons why I dislike SonarQube:
<ul>
<li>it does too many things. I like the Unix philosophy of simple tools that are specialized for the job. In this example, Checkstyle.</li>
<li>it runs as a service, which means I am dependent on it for my build to pass. If I'm outside the corporate network, I can't validate my code. If the service is down, I get a red build. I find it very counter-intuitive to rely on an online quality service instead of plain offline code tools.</li>
<li>its configuration, to the best of my knowledge, is done via the "friendly" web UI, where you can click to activate rules. I think it's easier to keep the configuration in the code. The configuration of individual rules can potentially be more complicated than what a UI can handle.</li>
<li>it doesn't play well with existing tools. At least in the JavaScript world, it was impossible to define the rules once in jscs and tell SonarQube to follow these rules.</li>
</ul>

In my opinion, it's a fancy tool with gimmicks like "you have 5 months of technical debt" to impress. It's definitely more impressive than an XML output report. But in the end I don't need a pretty graph, I need tools that help me pay back the debt, and that's TeamCity and its integration with established tools from the community.

<strong>Update</strong>: turns out Checkstyle ignores test code by default. You can set the <code>includeTestSourceDirectory</code> to true in the pom.xml in order to lint also test code. I have already updated the example pom.xml. This however will require commenting every unit test method, which might be a bit too much. Luckily this is easily fixable. In the checkstyle.xml, modify the JavadocMethod rule, so that it excludes methods with certain attributes. I've set it to allow missing comments for Override (it does it by default), Test and Before.
