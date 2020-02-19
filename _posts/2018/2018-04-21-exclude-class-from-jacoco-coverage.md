---
layout: post
title: Exclude class from JaCoCo coverage
date: 2018-04-21 12:40:20.000000000 +02:00
published: true
categories:
  - testing
tags:
  - jacoco
  - Java
  - maven
---

JaCoCo's `exclude` configuration works with classes, so the `.class` extension
is important when specifying the path.

Example:

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.5</version>
  <configuration>
    <excludes>
      <!-- exclude classes in package com.acme.models whose name starts with Spring -->
      <exclude>com/acme/models/Spring*</exclude>
      <!-- exclude classes in package com.acme.api whose name ends with Api -->
      <exclude>com/acme/api/*Api.class</exclude>
      <!-- exclude all classes in package com.acme.generated -->
      <exclude>com/acme/generated/**/*</exclude>
    </excludes>
  </configuration>
</plugin>
```
