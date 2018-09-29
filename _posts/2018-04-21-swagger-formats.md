---
layout: post
title: Swagger Formats
date: 2018-04-21 16:02:30.000000000 +02:00
parent_id: '0'
published: true
categories:
- Quick Code Tips
tags:
- swagger
author: Nikolaos Georgiou
---

Some handy format combinations with Swagger:

    type: string
    format: byte

Creates a property of type <code>byte[]</code> (but it is serialized as a string).

    type: integer
    format: int64

Creates a property of type <code>Long</code>.

    type: string
    format: date-time

Creates a property of type <code>OffsetDateTime</code> (when using the java8 date library).

    type: string
    format: date

Creates a property of type <code>LocalDate</code>.
