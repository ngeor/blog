---
layout: post
title: Using swagger code generator with maven
date: 2018-04-21 20:07:00.000000000 +02:00
parent_id: '0'
published: true
categories:
- Quick Code Tips
tags:
- Java
- maven
- Spring Boot
- swagger
author: Nikolaos Georgiou
---

Following up the <a href="{{ site.baseurl }}/2018/04/15/building-a-rest-api-with-swagger-and-spring-boot.html">previous post about swagger</a>, in this post I'm using the maven plugin version of swagger code generator.

<!--more-->

I like to keep it in a separate profile in the pom so it's only activated consciously when needed:

```xml
<profiles>
    <profile>
        <id>swagger</id>
        <build>
            <plugins>
                <plugin>
                    <groupId>io.swagger</groupId>
                    <artifactId>swagger-codegen-maven-plugin</artifactId>
                    <version>2.3.1</version>
                    <executions>
                        <execution>
                            <id>default-cli</id>
                            <goals>
                                <goal>generate</goal>
                            </goals>
                            <configuration>
                                <inputSpec>src/main/swagger/swagger.yml</inputSpec>
                                <language>spring</language>
                                <output>${project.basedir}</output>
                                <modelPackage>com.acme.blog.models</modelPackage>
                                <apiPackage>com.acme.blog.api</apiPackage>
                                <configOptions>
                                    <dateLibrary>java8</dateLibrary>
                                    <artifactId>blog</artifactId>
                                    <groupId>com.acme</groupId>
                                    <basePackage>com.acme.blog</basePackage>
                                    <configPackage>com.acme.blog.configuration</configPackage>
                                    <hideGenerationTimestamp>true</hideGenerationTimestamp>
                                </configOptions>
                            </configuration>
                        </execution>
                    </executions>
                </plugin>
            </plugins>
        </build>
    </profile>
</profiles>
```

and run it with <code>mvn -P swagger swagger-codegen:generate</code>
