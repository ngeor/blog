---
layout: post
title: Troubleshooting SSL - missing /root/.postgresql/root.crt
date: 2018-11-02
published: true
categories:
- programming
tags:
- Java
- Docker
- PostgreSQL
- SSL
- Azure
---

I run into a problem today trying to connect to an Azure PostgreSQL database.
The database enforces SSL connections ("SSL enforce status" = "ENABLED").

The Java/Spring Boot service could not connect to the database. It would crash
with an error message complaining that it could not find the certificate
`/root/.postgresql/root.crt`.

I tried various tricks which all failed miserably. I could disable the SSL
enforcement but that would not have been nice either.

When all else failed, I RTFM. According to [the documentation](https://www.postgresql.org/docs/9.6/static/libpq-ssl.html), the purpose of
this certificate is to check that the server certificate is signed by a trusted
certificate authority.

Since my application is packaged in a Docker image based on the standard JRE
image, I guessed that my image probably already has such a file somewhere. So,
I fired up a container with the JRE image:

```
docker run --rm -it openjdk:11-jre-slim bash
```

and inside the container, I searched for `crt` files:

```
root@e1a2141f5bb7:/# find . -type f -name "*.crt"
./etc/ssl/certs/ca-certificates.crt
./usr/share/ca-certificates/mozilla/AC_RAIZ_FNMT-RCM.crt
./usr/share/ca-certificates/mozilla/Izenpe.com.crt
./usr/share/ca-certificates/mozilla/Verisign_Class_3_Public_Primary_Certification_Authority_-_G3.crt
./usr/share/ca-certificates/mozilla/Starfield_Class_2_CA.crt
... the list goes on ...
```

I picked the first one, and modified by application's Dockerfile like this:

```
RUN mkdir -p /root/.postgresql
RUN ln -s /etc/ssl/certs/ca-certificates.crt /root/.postgresql/root.crt
```

And that did the trick! Hope this helps.
