---
layout: post
title: SDKMAN! on Windows
date: 2019-12-07
published: true
categories:
  - programming
tags:
  - Java
  - SDKMAN!
  - Windows
  - Visual Studio Code
  - IntelliJ IDEA
---

SDKMAN! manages multiple versions of Java related SDKs. In its
[homepage](https://sdkman.io/), it says it runs on any UNIX based platform, but
I gave it a try on Windows and it works quite fine there too.

In the [installation page](https://sdkman.io/install), it explains that it
basically needs bash to run, together with some tooling. I don't use Windows
Linux Subsystem or Cygwin, but I do use Git Bash. In fact, although I prefer
using Windows, I don't have much experience with Powershell and I prefer using
bash. I use [Hyper](https://hyper.is/) as my terminal and I have configured both
IntelliJ IDEA and Visual Studio Code to use Git Bash as a default.

The extra tooling that is needed consists of `zip`, `unzip`, `curl`, `tar` and
`gzip`. According to the installation page, MinGW can be used to provide this
tooling. In my case, I already had everything through one way or another:

```sh
$ which zip
/c/texlive/2019/bin/win32/zip

$ which unzip
/usr/bin/unzip

$ which curl
/mingw64/bin/curl

$ which tar
/usr/bin/tar

$ which gzip
/usr/bin/gzip
```

So I should be good to go. I opened up my terminal and run the installation
script:

```sh
$ curl -s "https://get.sdkman.io" | bash
```

The installation succeeds with no issues. At the end of the output, I see some
interesting information:

```
Added sdkman init snippet to /c/Users/ngeor/.bashrc
Attempt update of zsh profile...
Updated existing /c/Users/ngeor/.zshrc

All done!

Please open a new terminal, or run the following in the existing one:

    source "/c/Users/ngeor/.sdkman/bin/sdkman-init.sh"

Then issue the following command:

    sdk help
```

So it already modified my `.bashrc` and my `.zshrc` (which I didn't know I had,
as I don't use zsh). Following the instructions, I opened up a new terminal and
indeed the `sdk` command works as expected.

First, I installed a JDK:

```sh
$ sdk install java 11.0.5-zulu
```

This also works fine. I had to restart my terminal but it picks up the newly
installed JDK:

```sh
$ which java
/c/Users/ngeor/.sdkman/candidates/java/current/bin/java

$ which javac
/c/Users/ngeor/.sdkman/candidates/java/current/bin/javac

$ java -version
openjdk version "11.0.5" 2019-10-15 LTS
OpenJDK Runtime Environment Zulu11.35+15-CA (build 11.0.5+10-LTS)
OpenJDK 64-Bit Server VM Zulu11.35+15-CA (build 11.0.5+10-LTS, mixed mode)
```

This also reveals where SDKMAN! stores the SDKs it manages. A version of a SDK
is stored in a folder like `$HOME/.sdkman/candidates/[sdk]/[version]` and the
current version of the SDK is at `$HOME/.sdkman/candidates/[sdk]/current`.

At this point, I got enough confidence that SDKMAN! is going to work for the
rest of the tools I wanted to install (ant, maven, gradle and groovy). So I
first went ahead and deleted what I already had.

Regarding Java, I uninstalled all Oracle JDKs from Apps and Features of Windows.
For the rest, I was maintaining them by myself in a `C:\opt` folder where I
unzip programs that don't have an installer:

<img src="/assets/2019/12/2019-12-07 08_06_38-opt.png" alt="My opt folder" />

So I just went ahead and deleted ant, 3 version of Maven, gradle and groovy.
Then, I installed them with SDKMAN! and it just worked.

```sh
$ which ant
/c/Users/ngeor/.sdkman/candidates/ant/current/bin/ant

$ ant -version
Apache Ant(TM) version 1.10.1 compiled on February 2 2017

$ which mvn
/c/Users/ngeor/.sdkman/candidates/maven/current/bin/mvn

$ mvn --version
Apache Maven 3.6.3 (cecedd343002696d0abb50b32b541b8a6ba2883f)
Maven home: C:\Users\ngeor\.sdkman\candidates\maven\current
Java version: 11.0.5, vendor: Azul Systems, Inc., runtime: C:\Users\ngeor\.sdkman\candidates\java\current
Default locale: en_US, platform encoding: Cp1252
OS name: "windows 10", version: "10.0", arch: "amd64", family: "windows"

$ which gradle
/c/Users/ngeor/.sdkman/candidates/gradle/current/bin/gradle

$ gradle --version

------------------------------------------------------------
Gradle 6.0.1
------------------------------------------------------------

Build time:   2019-11-18 20:25:01 UTC
Revision:     fad121066a68c4701acd362daf4287a7c309a0f5

Kotlin:       1.3.50
Groovy:       2.5.8
Ant:          Apache Ant(TM) version 1.10.7 compiled on September 1 2019
JVM:          11.0.5 (Azul Systems, Inc. 11.0.5+10-LTS)
OS:           Windows 10 10.0 amd64

$ which groovy
/c/Users/ngeor/.sdkman/candidates/groovy/current/bin/groovy

$ groovy --version
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.codehaus.groovy.vmplugin.v7.Java7$1 (file:/C:/Users/ngeor/.sdkman/candidates/groovy/current/lib/groovy-2.5.8.jar) to constructor java.lang.invoke.MethodHandles$Lookup(java.lang.Class,int)
WARNING: Please consider reporting this to the maintainers of org.codehaus.groovy.vmplugin.v7.Java7$1
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective
access operations
WARNING: All illegal access operations will be denied in a future release
Groovy Version: 2.5.8 JVM: 11.0.5 Vendor: Azul Systems, Inc. OS: Windows 10
```

Side note: got to love that older programs use `-version` to show their version,
newer use `--version`, and the latest like docker and kubectl use just
`version`.

Having everything installed nicely, I cleaned up my `PATH` in Windows, which was
a bit messy. I prefer to modify the user and not the system environment
variables. This is the before picture:

<img src="/assets/2019/12/2019-12-07 07_58_30-before.png" alt="User environment variables, before cleanup" />

and this is the after (anything Java related is gone):

<img src="/assets/2019/12/2019-12-07 08_00_03-after.png" alt="User environment variables, after cleanup" />

There's also one path in the system variables that I removed:

<img src="/assets/2019/12/2019-12-07 08_00_49-system.png" alt="System environment variable" />

I also removed variables like `JAVA_HOME` and `M2_HOME`.

Okay. Short pause to see where we are now:

- Installed SDKMAN!
- Installed JDK, Ant, Maven, Gradle and Groovy with SDKMAN!
- Removed versions of everything that was not installed via SDKMAN!
- Cleaned up environment variables in Windows

At this point, everything works fine from Git Bash. So if I open up Hyper (or
Git Bash directly), I can use any of the commands I installed without a problem.

This isn't the case with cmd or Powershell. They use the Windows environment
variables to determine the current `PATH`. SDKMAN! enhances the `PATH` when bash
starts up on the fly, so the tools work there but not in cmd/Powershell. As I
mentioned in the beginning of the post, this isn't a problem for me as I prefer
to use bash. It is also trivial to go and edit the PATH in Windows and add some
directories. For example, for Java I would have to add
`C:\Users\ngeor\.sdkman\candidates\java\current\bin` and for Maven
`C:\Users\ngeor\.sdkman\candidates\maven\current\bin`. Note that by adding the
`current` version, I am still able to switch between multiple versions using
SDKMAN! without having to edit the Windows environment variables.

The next step is to configure my IDEs. I mostly use IntelliJ IDEA Community
Edition for Java. Sometimes I like to use Visual Studio Code as well, although
for Java it can be a bit heavy.

For IntelliJ IDEA, close all projects so you're at the welcome screen. From the
Configure button, select Structure for New Projects:

<img src="/assets/2019/12/2019-12-07 08_31_40-idea.png" alt="IntelliJ IDEA" />

There, you can add the JDK:

<img src="/assets/2019/12/2019-12-07 08_33_23-idea-sdk.png" alt="IntelliJ IDEA SDK" />

Notice that here I'm not using the `current` folder but the specific version
folder `11.0.5-zulu`. I can add multiple SDKs in IntelliJ and name them after
that version. I can have different projects in IntelliJ using different JDK
versions without having to mess with the `current` version.

For Visual Studio Code to work, you're gonna have to go and edit the environment
variables in Windows. Tip: press the Windows key, then type "env". Most likely,
you'll get a fast way to edit them:

<img src="/assets/2019/12/2019-12-07 10_47_28-env.png" alt="Windows start menu" />

I had to make two changes:

- Set `JAVA_HOME` to `C:\Users\ngeor\.sdkman\candidates\java\current`
- Add `C:\Users\ngeor\.sdkman\candidates\maven\current\bin` to my `PATH`

And this makes Visual Studio Code happy as well.

In conclusion, SDKMAN! works quite fine in Windows too. Its homepage perhaps
gets you scared that it only works on unix-based systems, but this isn't the
case.
