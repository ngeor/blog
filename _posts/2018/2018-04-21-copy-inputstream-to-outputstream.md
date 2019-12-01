---
layout: post
title: Copy InputStream to OutputStream
date: 2018-04-21 19:19:53.000000000 +02:00
published: true
categories:
- programming
tags:
- Java
---

To copy from a stream into a file:

```java
import java.nio.file.Files;
import java.nio.file.Path;

Files.copy(inputStream, path);
```

To copy from a stream into another stream, assuming you're using Spring:

```java
import org.springframework.util.StreamUtils;

StreamUtils.copy(inputStream, outputStream);
```
