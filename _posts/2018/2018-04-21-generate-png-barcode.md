---
layout: post
title: Generate PNG barcode
date: 2018-04-21 19:35:51.000000000 +02:00
published: true
tags:
  - barcode
  - java
  - png
---

How to generate PNG barcodes in Java using the zxing library:

<!--more-->

Using the <a href="https://github.com/zxing/zxing">zxing</a> library in the pom:

```xml
<dependency>
    <groupId>com.google.zxing</groupId>
    <artifactId>core</artifactId>
    <version>3.3.2</version>
</dependency>
<dependency>
    <groupId>com.google.zxing</groupId>
    <artifactId>javase</artifactId>
    <version>3.3.2</version>
</dependency>
```

it is possible to generate a PNG barcode in various formats like this:

```java
Path barcode = tempDirectory.resolve("barcode.png");
BitMatrix bitMatrix = new Code39Writer().encode("data", BarcodeFormat.CODE_39, 204, 70);
MatrixToImageWriter.writeToPath(bitMatrix, "png", barcode);
```
