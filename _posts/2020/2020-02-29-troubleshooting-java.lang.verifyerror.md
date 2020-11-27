---
layout: post
title: Troubleshooting java.lang.VerifyError
date: 2020-02-29 08:31:56 +02:00
tags:
  - troubleshooting
  - java
  - verifyError
  - mockserver
  - dependencies
  - maven
---

Yesterday I got an exception I hadn't seen before,
[java.lang.VerifyError](https://docs.oracle.com/javase/8/docs/api/java/lang/VerifyError.html).

The stacktrace looked quite spicy, I had never seen anything like this:

```
java.lang.VerifyError: Stack map does not match the one at exception handler 118
Exception Details:
 Location:
   com/acme/MyClass.runQuery(Ljava/lang/String;Ljava/time/LocalDate;)D @118: astore
 Reason:
   Type 'org/json/JSONException' (current frame, stack[0]) is not assignable to 'java/lang/RuntimeException' (stack map, stack[0])
 Current Frame:
   bci: @36
   flags: { }
   locals: { 'com/acme/MyClass', 'java/lang/String', 'java/time/LocalDate', 'java/time/ZoneId', 'java/util/Map', 'org/json/JSONObject' }
   stack: { 'org/json/JSONException' }
 Stackmap Frame:
   bci: @118
   flags: { }
   locals: { 'com/acme/MyClass', 'java/lang/String', 'java/time/LocalDate', 'java/time/ZoneId', 'java/util/Map', 'org/json/JSONObject' }
   stack: { 'java/lang/RuntimeException' }
 Bytecode:
   0000000: 1210 b800 114e 1212 2c2d b600 13b6 0014
   0000010: b800 15b8 0016 3a04 2ab4 0004 2b19 04b6
   0000020: 0017 3a05 1905 1218 b600 193a 0612 1a19
   0000030: 06b6 001b 9a00 11b2 0006 121c 1906 b900
   0000040: 0f03 000e af19 0512 1db6 001e 3a07 1907
   0000050: 121f b600 203a 0819 0803 b600 213a 0919
   0000060: 0912 22b6 0020 3a0a 190a 04b6 0023 3a0b
   0000070: 190b b800 24af 3a06 b200 0612 2719 06b6
   0000080: 0028 b900 0f03 000e af
 Exception Handler Table:
   bci [36, 68] => handler: 118
   bci [36, 68] => handler: 118
   bci [69, 117] => handler: 118
   bci [69, 117] => handler: 118
 Stackmap Table:
   full_frame(@69,{Object[#48],Object[#90],Object[#91],Object[#92],Object[#93],Object[#94],Object[#90]},{})
   full_frame(@118,{Object[#48],Object[#90],Object[#91],Object[#92],Object[#93],Object[#94]},{Object[#95]})
    at com.acme.Fetcher.<init>(Fetcher.java:38)
    at com.acme.Fetcher.<init>(Fetcher.java:53)
    [ ... ]
```

This is new to me but clearly an exception that provides **bytecode** as
relevant information can only mean trouble. Doing a search on the web does not
return many results but
[this StackOverflow post](https://stackoverflow.com/questions/100107/causes-of-getting-a-java-lang-verifyerror)
gave me some hint:

> `java.lang.VerifyError` can be the result when you have compiled against a
> different library than you are using at runtime

A closer inspection of the exception shows this message:

> `Type 'org/json/JSONException' (current frame, stack[0]) is not assignable to 'java/lang/RuntimeException'`

So maybe somehow I'm using the wrong version of the
[org.json](https://github.com/stleary/JSON-java) library?

I run `mvn dependency:tree` to see if something looks fishy, but everything is
fine. There is only one version of `org.json` in the dependency tree and it is
the correct one. Where is the wrong version of `org.json.JSONException` coming
from then?

Backtracking changes to the `pom.xml`, I saw that a few hours earlier I had
added a new dependency,
[mockserver-netty](https://github.com/mock-server/mockserver). This is a mock
server, useful for integration tests. Of course, I had added it as a test
dependency, so that should not be the problem, right?

Turns out, this was the problem.

Our Dockerfile copied all jars from the `target/lib` folder into the Docker
image of the application. And we were using the
[Maven dependency plugin](https://maven.apache.org/plugins/maven-dependency-plugin/copy-dependencies-mojo.html)
to copy the dependencies into the `target/lib` folder. But, the setting
`includeScope` was not set, so it was using the default, which is `test`. So
even though I had added a new _test_ dependency, it was being packaged inside
the Docker image and it was on the class path at runtime.

But when I run `mvn dependency:tree`, there is no other mention of `org.json`.
How is then `mockserver` causing this problem? Where is this other
`org.json.JSONException` coming from? And then I realized something **bad** is
going on. `mockserver` or one of its dependencies is defining its own
`org.json.JSONException` class and this is causing the collision.

To validate the hypothesis, I run this command for every jar file in
`target/lib`: `unzip -l | grep org/json` (so I'm listing the contents of each
jar, which is just a zip file, and grepping for org/json). Bingo. There is
another package which implements `org.json.JSONException` (and a few more
`org.json` classes), it's `com.vaadin.external.google:android-json`:

```
[INFO] \- org.mock-server:mockserver-netty:jar:5.9.0:test
[INFO]    +- org.mock-server:mockserver-core:jar:5.9.0:test
[INFO]    |  +- org.skyscreamer:jsonassert:jar:1.5.0:test
[INFO]    |  |  \- com.vaadin.external.google:android-json:jar:0.0.20131108.vaadin1:test
```

At this point I'm able to fix my application, and confirm I'm not going crazy,
by setting `<includeScope>runtime</includeScope>` in my `pom.xml`, which
excludes all the test dependencies from being deployed to production.

As a next step, I investigated the `org.skyscreamer:jsonassert` dependency and
found that it comes from
[this repository](https://github.com/skyscreamer/JSONassert) which looks
abandoned. It doesn't have any new commits in the past 3 years (one could argue
if the lack of activity indicates abandonment or not). The issue I wanted to
raise was already raised
[2 years ago](https://github.com/skyscreamer/JSONassert/issues/99). So I doubt
anything will change anytime soon.

I then went to the next dependency, which is `mockserver-core`. I submitted
[an issue](https://github.com/mock-server/mockserver/issues/738) myself
immediately and hopefully this can be fixed in the future.

So, what are the lessons of this story?

- the answer is always in the stacktrace/logs
- assumption is the root of all evil (I had assumed our test dependencies
  weren't in the classpath on prod)
- whether you're working on your app or publishing a library for others, it's
  important to check what dependencies you're bringing with you and that those
  dependencies are secure and up to date
