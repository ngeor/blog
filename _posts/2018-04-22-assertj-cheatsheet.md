---
layout: post
title: AssertJ cheatsheet
date: 2018-04-22 07:10:29.000000000 +02:00
published: true
categories:
- Quick Code Tips
tags:
- AssertJ
- Java
- unit tests
---

<a href="https://joel-costigliola.github.io/assertj/">AssertJ</a> is a an assertions library for unit tests in Java that is well worth considering. Here are some examples.

<!--more-->
<h3>Basic</h3>

```java
import static org.assertj.core.api.Assertions.assertThat;

assertThat(something).isNotNull();
assertThat(something).isNull();
assertThat(something).isEqualTo(expectation);
assertThat(something.getId()).isGreaterThan(0);
```
<h3>Exceptions</h3>

```java
import static org.assertj.core.api.Assertions.assertThatThrownBy;

assertThatThrownBy(() -> obj.action())
    .isInstanceOf(IOException.class);

assertThatThrownBy(() -> obj.otherAction())
    .isInstanceOf(TimeoutException.class)
    .hasMessage("oops")
    .hasFieldOrPropertyWithValue("code", HttpStatus.GATEWAY_TIMEOUT);
```
<h3>Dates</h3>

```java
import java.time.OffsetDateTime;
import java.time.temporal.ChronoUnit;
import static org.assertj.core.api.Assertions.within;

assertThat(obj.getCreatedAt())
    .isCloseTo(OffsetDateTime.now(), within(500, ChronoUnit.MILLIS));
```
<h3>Projections</h3>

```java
assertThat(result.getParcels())
    .extracting(Parcel::getWeight)
    .isEqualTo(Arrays.asList(new BigDecimal(10), new BigDecimal(20)));
```
