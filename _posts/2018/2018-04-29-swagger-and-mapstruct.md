---
layout: post
title: Swagger and MapStruct
date: 2018-04-29 14:39:53.000000000 +02:00
published: true
categories:
- programming
tags:
- java
- MapStruct
- maven
- swagger
---

I've been working lately on a project with a few services (or microservices, if you like to play buzzword bingo). I wanted to share some thoughts on how using Swagger together with MapStruct can make things easier.

<!--more-->

First of all, consider the setup. We have a two services, A and B. Each service has its own code repository, each is deployed independently from the other. They are both on Java 8 with Spring Boot 2. They both use Swagger to generate a lot of boilerplate code and to offer a live documentation of their API.

Service A wants to call service B. This is the typical workflow:
<ul>
<li>the user sends a POST request to service A with object X</li>
<li>service A sends a POST request to service B with object X'</li>
<li>service B return reply Y'</li>
<li>service A returns reply Y</li>
</ul>

In reality, objects X and X' (just like Y and Y') are very similar. In fact, in the beginning of my project they were identical. However, they are owned by different services and they can - and will - evolve independently.

It is very tempting in the implementation of service A to do something like this:

```java
import serviceA.models.X;
import serviceA.models.Y;

Y callServiceB(X request) {
    Y response = http.call(urlOfServiceB, request);
    return response;
}
```

But this is wrong, because in reality you should be communicating with service B using its own schema. This is like mixing persistent data objects with domain models because they are 'almost' the same.

A more accurate representation of what we should be doing looks like this:

```java
import serviceA.models.X;
import serviceA.models.Y;
import serviceB.models.X;
import serviceB.models.Y;

serviceA.models.Y callServiceB(serviceA.models.X request) {
    serviceB.models.X mappedRequest = map(request);
    serviceB.models.Y response = http.call(urlOfServiceB, mappedRequest);
    serviceA.models.Y mappedResponse = map(response);
    return mappedResponse;
}
```

Now this is better, but it can lead to a lot of boring mapping code:

```java
serviceB.models.X map(serviceA.models.X request) {
    serviceB.models.X mapped = new serviceB.models.X();
    mapped.setId(request.getId());
    mapped.setFullName(request.getFullName());
    // and so on
    return mapped;
}
```

This is where a tool called <a href="http://mapstruct.org/">MapStruct</a> comes to save the day. MapStruct generates the boring mapping logic for you. In this particular case, where the mapped objects are let's say 90% identical, you'll barely have to write any code:

```java
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface AwesomeModelMapper {

    AwesomeModelMapper INSTANCE = Mappers.getMapper(AwesomeModelMapper.class);

    serviceB.models.X mapRequest(serviceA.models.X request);

    serviceA.models.Y mapResponse(serviceB.models.Y response);

}
```

This will generate the boring code automatically for you. To integrate it in Maven, add this to the pom:

```xml
<properties>
    <org.mapstruct.version>1.2.0.Final</org.mapstruct.version>
</properties>

<dependency>
    <groupId>org.mapstruct</groupId>
    <artifactId>mapstruct-jdk8</artifactId>
    <version>${org.mapstruct.version}</version>
</dependency>

<dependency>
    <groupId>org.mapstruct</groupId>
    <artifactId>mapstruct-processor</artifactId>
    <version>${org.mapstruct.version}</version>
    <scope>provided</scope>
</dependency>
```

Note that it generates the code at compile time and you can see it under the folder <code>target/generated-sources/annotations</code>.

Having solved the boring part, this is how I have configured Swagger for service A to use service B:

```xml
<plugin>
    <groupId>io.swagger</groupId>
    <artifactId>swagger-codegen-maven-plugin</artifactId>
    <version>${swagger-codegen-maven-plugin.version}</version>
    <executions>
        <execution>
            <id>client-b</id>
            <goals>
                <goal>generate</goal>
            </goals>
            <configuration>
                <inputSpec>src/main/swagger/client-b.yml</inputSpec>
                <language>java</language>
                <output>${project.build.directory}/generated-sources/client-b</output>
                <modelPackage>serviceB.models</modelPackage>
                <apiPackage>serviceB.api</apiPackage>
                <invokerPackage>serviceB</invokerPackage>
                <generateApiTests>false</generateApiTests>
                <modelNameSuffix>ClientModel</modelNameSuffix>
                <configOptions>
                    <dateLibrary>java8</dateLibrary>
                    <library>resttemplate</library>
                    <artifactId>client-b</artifactId>
                    <groupId>com.acme</groupId>
                    <basePackage>serviceB</basePackage>
                    <configPackage>sericeB.configuration</configPackage>
                </configOptions>
            </configuration>
        </execution>
    </executions>
</plugin>
```

Points of interest:
<ul>
<li>this is an additional execution of the Swagger code generation plugin, which generates the client code that calls service B. Service A already has its own swagger code generation which generates the server code (you can see it in <a href="{{ site.baseurl }}/2018/04/21/using-swagger-code-generator-with-maven.html">a previous post</a>).</li>
<li>

the Swagger definition <code>client-b.yml</code> is copy pasted (gasp!) from service B. If service B introduces a new operation or a new field, it won't be available until service A updates itself. If service B introduces a new mandatory field, service A will break. There are various ways to ensure the services don't break. For example, you can introduce mandatory fields in phases: phase 1, the field is introduced as optional. When all clients have upgraded, phase 2, change the field into mandatory. On a side note about backwards compatible changes, my VB6 apps (the exe files) still run in Windows 10.
</li>
<li>

the models are suffixed with <code>ClientModel</code> to avoid fully qualifying classes by package name as I did in the pseudo-code above.
</li>
<li>

the code that is generated by this execution is not committed in the VCS.
</li>
</ul>

What about testing? Surely, if MapStruct generates all these awesome mappers automatically, we don't even need to write unit tests for the mapping logic anymore, right? I would say unfortunately that's not the case.

First of all, you were going to write the unit tests anyway, so it's not like you're doing any extra work (just trying to make you feel better).

The thing is, all the code in question is automatically generated:
<ul>
<li>models of service A are generated by Swagger</li>
<li>models of service B are also generated by Swagger, with a different configuration</li>
<li>the mapping logic between them is generated by MapStruct</li>
</ul>

The thing is MapStruct will only complain if a property has the same name of both models but different types (and additionally it doesn't know how to map from type to type). It won't complain for example about fields that don't have a counterpart in the other class. So if we introduce a new field in service B's YML, everything will still compile, but that field will stay null forever.

I think this is the type of scenarios we should be guarding against. I used the following technique:

First, generate mappers in both directions, even if they're not needed. They will be needed for this test:

```java
@Mapper
public interface AwesomeModelMapper {

    serviceB.models.X a2b(serviceA.models.X request);

    serviceA.models.X b2a(serviceB.models.X request);
}
```

Now the test goes like this:
<ul>
<li>create an instance of serviceA.models.X</li>
<li>fill all properties with non-null values (possibly recursively)</li>
<li>convert it to service B's flavor</li>
<li>convert it back to service A</li>
<li>the resulting object should be still identical to the original. If some fields turned out to be null, someone has introduced a new property in A but not in B.</li>
</ul>

With some creative use of reflection, you can go far in creating this type of tests that will save you from headaches.

In any case, my take on this is to test the mappers, even if they're automatically generated.
