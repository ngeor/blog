---
layout: post
title: Using Spring Boot Actuators
date: 2018-07-07 08:38:06.000000000 +02:00
parent_id: '0'
published: true
categories:
- Code
tags:
- actuators
- Java
- Spring Boot
author: Nikolaos Georgiou
---

Implementing Spring Boot actuators is not very difficult. In this post I'll show what you can get for free, without adding any code.

<!--more-->

First of all, you need this dependency in your <code>pom.xml</code>:

```xml
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
```

This will expose the <code>/health</code> and <code>/info</code> endpoints by default, as mentioned in <a href="https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-endpoints.html">the documentation</a>. Both endpoints will be under <code>/actuator</code> (so the full path is <code>/actuator/health</code>).

<strong>Health endpoint</strong>

The health endpoint will give back this JSON:

```
{"status":"UP"}
```

which tells us that the service is up and running.

<strong>Info endpoint</strong>

The info endpoint does not return any information by default. We can change that and use the endpoint to see the state of the git repository at the time of the build.

In <code>pom.xml</code>, add the following build plugin:

```xml
      <plugin>
        <groupId>pl.project13.maven</groupId>
        <artifactId>git-commit-id-plugin</artifactId>
      </plugin>
```

and in <code>application.properties</code>, add this line:

```
management.info.git.mode=full
```

Now, the info endpoint will offer information about the state of the git repository at the time the project was built.

Example:

```
{
  "git": {
    "build": {
      "host": "6b7e5600-3108-4330-a08a-5a7eff38002d",
      "version": "1.0.0",
      "time": "2018-07-06T09:59:47Z",
      "user": {
        "name": "",
        "email": ""
      }
    },
    "branch": "master",
    "commit": {
      "message": {
        "short": "Merged in MON-448 (pull request #3)",
        "full": "Merged in MON-448 (pull request #3)\n\nMON-448 Changed auth service to return ExpiresIn for the access token."
      },
      "id": {
        "describe": "df38293",
        "abbrev": "df38293",
        "describe-short": "df38293",
        "full": "df382933d0e2f8cb390cfe9f2e87e6a9046b661d"
      },
      "time": "2018-07-06T09:59:07Z",
      "user": {
        "email": "john.doe@wordpress.com",
        "name": "John Doe"
      }
    },
    "closest": {
      "tag": {
        "name": "",
        "commit": {
          "count": ""
        }
      }
    },
    "dirty": "false",
    "remote": {
      "origin": {
        "url": "https://github.com/secret-project.git"
      }
    },
    "tags": ""
  }
}
```

<strong>Adding more endpoints</strong>

There are more endpoints available, but not exposed by default. As an example, let's enable the metrics endpoint. We need this in <code>application.properties</code>:

```
management.endpoint.metrics.enabled=true
management.endpoints.web.exposure.include=health,info,metrics
```

This will enable the metrics endpoint but also expose it through the web.

Alternatively, we can expose all endpoints to the web, but control which ones are enabled:

```
management.endpoints.web.exposure.include=*
management.endpoints.enabled-by-default=false
management.endpoint.health.enabled=true
management.endpoint.info.enabled=true
management.endpoint.metrics.enabled=true
```

<strong>Metrics endpoint</strong>

In any case, visiting the endpoint at <code>/actuators/metrics</code> give us a list of available metrics:

```
{
  "names": [
    "http.server.requests",
    "process.files.max",
    "jvm.gc.memory.promoted",
    "tomcat.cache.hit",
    "jvm.memory.committed",
    "system.load.average.1m",
    "tomcat.cache.access",
    "jvm.memory.used",
    "jvm.gc.max.data.size",
    "system.cpu.count",
    "logback.events",
    "tomcat.global.sent",
    "jvm.buffer.memory.used",
    "tomcat.sessions.created",
    "jvm.memory.max",
    "jvm.threads.daemon",
    "system.cpu.usage",
    "jvm.gc.memory.allocated",
    "tomcat.global.request.max",
    "tomcat.global.request",
    "tomcat.sessions.expired",
    "jvm.threads.live",
    "jvm.threads.peak",
    "tomcat.global.received",
    "process.uptime",
    "tomcat.sessions.rejected",
    "process.cpu.usage",
    "jvm.gc.pause",
    "tomcat.threads.config.max",
    "jvm.classes.loaded",
    "jvm.classes.unloaded",
    "tomcat.global.error",
    "tomcat.sessions.active.current",
    "tomcat.sessions.alive.max",
    "jvm.gc.live.data.size",
    "tomcat.servlet.request.max",
    "tomcat.threads.current",
    "tomcat.servlet.request",
    "process.files.open",
    "jvm.buffer.count",
    "jvm.buffer.total.capacity",
    "tomcat.sessions.active.max",
    "tomcat.threads.busy",
    "process.start.time",
    "tomcat.servlet.error"
  ]
}
```

And to see for example the uptime (<code>process.uptime</code> metric) we need to visit <code>/actuator/metrics/process.uptime</code>:

```
{
  "name": "process.uptime",
  "measurements": [
    {
      "statistic": "VALUE",
      "value": 72704.929
    }
  ],
  "availableTags": []
}
```

<strong>Security</strong>

Some endpoints might reveal sensitive information that can potentially be exploited by an attacker. If Spring Security is used, the actuators are protected by default.

You can bypass Spring Security for the actuators that you feel comfortable that they do not expose anything exploitable. You'll need this kind of configuration:

```java
@EnableWebSecurity
public class SecurityConfiguration extends WebSecurityConfigurerAdapter {
    private static final String[] AUTH_WHITELIST = {
        "/actuator/info",
        "/actuator/health"
        // other public endpoints of your API may be appended to this array
    };

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        // allow all whitelisted resources
        http.authorizeRequests().antMatchers(AUTH_WHITELIST).permitAll();
    }
}
```

<strong>Conclusion</strong>

It's easy to get started with Spring Boot actuators, without even writing any code. You can already use these endpoints in monitoring tools, but also extend them with <a href="https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-endpoints.html#production-ready-endpoints-custom">custom solutions</a>.
