---
layout: post
title: Code coverage on integration tests?
date: 2018-08-11 19:48:15.000000000 +02:00
published: true
categories:
- Code
tags:
- code coverage
- integration tests
- jacoco
- java
- maven
- unit tests
---

Should you collect and measure code coverage on integration tests or only unit tests? In this post I'll share some thoughts on this topic.

<!--more-->

Unit tests are tests which exercise a single unit of code in isolation. In my case, the programming language is Java, so the smallest unit of code is a class. All external dependencies to the class being tested (<em>system under test</em>) should be replaced with test doubles (stubs, mocks).

Integration tests on the other hand exercise multiple units of code together. Again, in my case, the context is Spring Boot. It's very easy to test the entire actual application with Spring Boot.

Going from a unit test to an integration test is not a binary divide but a spectrum. As we broaden the testing boundary, we shift from testing a unit to testing a group. For example, we might have an integration test which focuses on the interaction of the database layer with an actual database, while mocking some other parts. Or, we might have a test which is not using test doubles but its actual dependencies. There is a place for these tests, the only challenge being how to call them.

To keep things simple here, by integration test I mean testing the entire Spring Boot application.

As unit tests operate on a single unit of code, without using real external dependencies, they are typically very fast and they can be - and should be - exhaustive.

Integration tests on the other hand are much slower, but they can test the application under real conditions, test HTTP protocol interaction, etc.

Going back to code coverage, code coverage is nothing more but checking which lines of code were executed during a test run. A single integration test might be hitting a great amount of lines of code, giving a big boost of code coverage. However, as the test is not focusing on little details, it is possible that a unit is slightly modified in an undesired way and the test might still be pass.

As unit tests are cheaper, they allow to write thorough tests for each unit in isolation. That is why it makes more sense to measure code coverage on the unit tests. It is more likely that a line that has been visited (covered) has actually been tested and it hasn't just been visited by coincidence.

The same principle applies to fixing a bug: if it is possible, a bug should be fixed with a unit test.

Is there a reason why you should measure code coverage on integration tests? I think there might be. I've been practicing the following technique:
<ul>
<li>measure code coverage (and code complexity) on unit tests</li>
<li>generate the code coverage report</li>
<li>measure code coverage (but not code complexity) on integration tests</li>
<li>generate the <strong>aggregate</strong> code coverage report, unit and integration tests combined</li>
</ul>

While I don't obsess on how much my code coverage is on the first report, the second report <em>should</em> be nearing 100% code coverage. There is always going to be some code that can't be tested with unit tests and that is <strong>totally fine</strong>. I don't think we should write awkward code to try to unit test code that was not meant to be unit tested. However, if the aggregate code coverage report isn't hitting almost 100% code coverage, then you either have really forgotten to write some tests, or you might have uncovered some code that can be deleted. Nothing better than deleting some unused code.

Now, time for some code. Step by step, this is what my JaCoCo configuration looks like in <code>pom.xml</code>:

<code>pre-unit-test</code> starts the JaCoCo agent before the unit tests are run:

```xml
<execution>
  <id>pre-unit-test</id>
  <goals>
    <goal>prepare-agent</goal>
  </goals>
</execution>
```

<code>post-unit-test</code> generates the unit test code coverage report after the unit tests pass:

```xml
<execution>
  <id>post-unit-test</id>
  <phase>test</phase>
  <goals>
    <goal>report</goal>
  </goals>
</execution>
```

<code>check-unit-test</code> breaks the build if the code coverage is not good enough, according to the configured standards (code complexity is also a reason to break the build):

```xml
<execution>
  <id>check-unit-test</id>
  <phase>test</phase>
  <goals>
    <goal>check</goal>
  </goals>
  <configuration>
    <dataFile>${project.build.directory}/jacoco.exec</dataFile>
    <rules>
      <rule>
        <element>BUNDLE</element>
        <limits>
          <limit>
            <counter>INSTRUCTION</counter>
            <value>COVEREDRATIO</value>
            <minimum>${jacoco.unit-tests.limit.instruction-ratio}</minimum>
          </limit>
          <limit>
            <counter>BRANCH</counter>
            <value>COVEREDRATIO</value>
            <minimum>${jacoco.unit-tests.limit.branch-ratio}</minimum>
          </limit>
        </limits>
      </rule>
      <rule>
        <element>CLASS</element>
        <limits>
          <limit>
            <counter>COMPLEXITY</counter>
            <value>TOTALCOUNT</value>
            <maximum>${jacoco.unit-tests.limit.class-complexity}</maximum>
          </limit>
        </limits>
      </rule>
      <rule>
        <element>METHOD</element>
        <limits>
          <limit>
            <counter>COMPLEXITY</counter>
            <value>TOTALCOUNT</value>
            <maximum>${jacoco.unit-tests.limit.method-complexity}</maximum>
          </limit>
        </limits>
      </rule>
    </rules>
  </configuration>
</execution>
```

<code>pre-integration-test</code> prepares the JaCoCo agent for the integration tests:

```xml
<execution>
  <id>pre-integration-test</id>
  <goals>
    <goal>prepare-agent-integration</goal>
  </goals>
</execution>
```

<code>post-integration-test</code> runs the report for integration tests:

```xml
<execution>
  <id>post-integration-test</id>
  <goals>
    <goal>report-integration</goal>
  </goals>
</execution>
```

<code>merge-results</code> will merge the code coverage results of unit and integration tests into a new file, <code>aggregate.exec</code>:

```xml
<execution>
  <id>merge-results</id>
  <phase>verify</phase>
  <goals>
    <goal>merge</goal>
  </goals>
  <configuration>
    <fileSets>
      <fileSet>
        <directory>${project.build.directory}</directory>
        <includes>
          <include>*.exec</include>
        </includes>
        <excludes>
          <exclude>aggregate.exec</exclude>
        </excludes>
      </fileSet>
    </fileSets>
    <destFile>${project.build.directory}/aggregate.exec</destFile>
  </configuration>
</execution>
```

<code>post-merge-report</code> will generate the report for the aggregate coverage:

```xml
<execution>
  <id>post-merge-report</id>
  <phase>verify</phase>
  <goals>
    <goal>report</goal>
  </goals>
  <configuration>
    <dataFile>${project.build.directory}/aggregate.exec</dataFile>
    <outputDirectory>${project.reporting.outputDirectory}/jacoco-aggregate</outputDirectory>
  </configuration>
</execution>
```

<code>check-aggregate</code> will break the build if the aggregate code coverage is not good enough:

```xml
<execution>
  <id>check-aggregate</id>
  <phase>verify</phase>
  <goals>
    <goal>check</goal>
  </goals>
  <configuration>
    <dataFile>${project.build.directory}/aggregate.exec</dataFile>
    <rules>
      <rule>
        <element>BUNDLE</element>
        <limits>
          <limit>
            <counter>INSTRUCTION</counter>
            <value>COVEREDRATIO</value>
            <minimum>${jacoco.aggregate.limit.instruction-ratio}</minimum>
          </limit>
          <limit>
            <counter>BRANCH</counter>
            <value>COVEREDRATIO</value>
            <minimum>${jacoco.aggregate.limit.branch-ratio}</minimum>
          </limit>
        </limits>
      </rule>
    </rules>
  </configuration>
</execution>
```

The thresholds are using properties, so that they can be clearly defined in the properties section of the pom. This also allows for some streamlining of the configuration, by placing JaCoCo's configuration in a parent pom and leaving only the threshold properties in the child pom.
