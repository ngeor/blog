---
layout: post
title: Verify void method with Mockito
date: 2018-04-21 12:38:39.000000000 +02:00
type: post
parent_id: '0'
published: true
categories:
- Quick Code Tips
tags:
- Java
- mockito
author: Nikolaos Georgiou
---

To verify a method that returns <code>void</code> with Mockito, you need to do this:

```java
Mockito.verify(myMock).myVoidMethod();
```
