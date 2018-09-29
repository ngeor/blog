---
layout: post
title: Exclude class from JaCoCo coverage
date: 2018-04-21 12:40:20.000000000 +02:00
parent_id: '0'
published: true
categories:
- Quick Code Tips
tags:
- JaCoCo
- Java
- maven
author: Nikolaos Georgiou
---

JaCoCo's <code>exclude</code> configuration works with classes, so the <code>.class</code> extension is relevant in specifying the path.

Example:

```xml

<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.1</version>
    <configuration>
        <excludes>
            <exclude>com/acme/models/Spring*</exclude>

            <exclude>com/acme/api/*Api.class</exclude>

            <exclude>com/acme/generated/**/*</exclude>

        </excludes>
    </configuration>

```
