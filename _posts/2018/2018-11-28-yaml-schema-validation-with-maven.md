---
layout: post
title: YAML schema validation with Maven
date: 2018-11-28
published: true
categories:
  - consistency
tags:
  - Java
  - maven
  - swagger
  - yaml
  - json
  - microservices
  - ci-tooling
---

Sometimes it feels we're reinventing the wheel, but with different names. Back
in the days, XML was the cool thing. We had XPath as a query language. We had
XSLT to transform XML documents into different shapes. We had XSD to validate
the schema of XML. We had code generation and validation. We could generate web
service clients and servers with WSDL.

But then, people started hating angle brackets I suppose. We switched to JSON,
because curly brackets are prettier. We still called it AJAX, because AJAJ was
too difficult to pronounce I guess. JSON is the standard content type for pretty
much any web service call.

A few seconds later, we now don't like curly brackets either and YAML is the new
kid on the block. At least for configuration files, JSON isn't cool anymore.

The problem with the latest and greatest is that it lacks the maturity of the
old and tried. Some developers are eager to jump on anything that has that cool
factor, regardless of its maturity and adoption (and regardless of whether it's
the right tool for the job anyway).

In my case, I have some YAML files that I would like to validate. These are my
Swagger definitions and I would like to perform some checks. Take these two for
example:

- all operations need to be documented (i.e. the `description` property needs to
  be mandatory), so that my API can be understood by its users.
- all URL paths need to be lower case, separated by hyphens, so that the API is
  consistent.

It would be great if I don't have to write any code to support this... and the
search begins.

## Searching for YAML validation

Googling around for a YAML schema validator does not bring many results (what a
surprise). We have some candidates:

- [Rx](http://rx.codesimply.com/)
- [Kwalify](http://www.kuwata-lab.com/kwalify/)
- [JSON Schema](https://json-schema-everywhere.github.io/yaml)

The first two don't have tooling for Java (Java lacks the cool factor so the
cool kids don't bother with it) and/or are not maintained anymore.

The third option is a bit of a workaround. YAML is a superset of JSON. If I'm
not using anything fancy (and I don't think I am), I should be able to convert
the YAML file into a JSON and then use [JSON schema](https://json-schema.org/),
which has good adoption.

## Converting YAML to JSON

I did some investigation here as well and I couldn't find an existing Maven
plugin. The code to [convert YAML to JSON is trivial with
Jackson](https://stackoverflow.com/questions/23744216/how-do-i-convert-from-yaml-to-json-in-java)
so I put together a [tiny Maven
plugin](https://github.com/ngeor/yak4j-json-yaml-converter-maven-plugin) which
does exactly that and nothing more.

## Validating JSON schema

When it comes to performing JSON schema validation, I found two existing Maven
plugins, one from [Groupon](https://github.com/groupon/json-schema-validator)
and one from
[Collaborne](https://github.com/Collaborne/json-schema-validator-maven-plugin).
As the first one is more recently maintained, I gave that one a chance and it
worked.

## Writing the JSON schema

With a little bit of reading, I came up with the following initial version of my
schema:

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "description": "Validate Swagger documents",
  "type": "object",
  "properties": {
    "swagger": {
      "type": "string"
    },
    "paths": {
      "type": "object",
      "patternProperties": {
        "^/[a-z-]+(/(([a-z-]+)|({[a-zA-Z]+})))*$": {
          "type": "object",
          "patternProperties": {
            "^get|post|put|delete$": {
              "type": "object",
              "required": ["operationId", "description"],
              "properties": {
                "operationId": {
                  "type": "string"
                },
                "description": {
                  "type": "string"
                }
              }
            },
            "^parameters$": {
              "type": "array"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    }
  },
  "required": ["swagger", "paths"]
}
```

It's quite powerful (and it works). I didn't spend more than 10' so it can
definitely be improved. The URL path validation is done with the regular
expression: `"^/[a-z-]+(/(([a-z-]+)|({[a-zA-Z]+})))*$"`. Regular expressions
can be cryptic so what this says is that:

- URL paths need to start with /
- only lower case, only hyphens
- subsequent path segments can contain a variable placeholder `{blah}` which
  is in camelCase

We also check that the allowed verbs are `get`, `post`, `put` and `delete`, and
that the `description` property is mandatory.

## Reusing the schema

If you've gone this far, you probably want to reuse this schema file in all of
your microservices. To avoid copy pasting it around, we can package it in a tiny
JAR file all by itself. I made a new git repository, with its own pipeline and
versioning, which just publishes this schema to Nexus.

The Groupon plugin unfortunately can only read files from the local filesystem
(I've opened a [feature
request](https://github.com/groupon/json-schema-validator/issues/7)), but we can
use the Maven dependency plugin to unpack the shared schema artifact manually
and bring them in place before the Groupon plugin kicks in:

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-dependency-plugin</artifactId>
  <version>3.1.1</version>
  <executions>
    <execution>
      <id>unpack</id>
      <phase>validate</phase>
      <goals>
        <goal>unpack</goal>
      </goals>
      <configuration>
        <artifactItems>
          <artifactItem>
            <groupId>com.acme</groupId>
            <artifactId>acme-swagger-schema</artifactId>
            <version>0.0.1</version>
            <type>jar</type>
            <outputDirectory>${project.build.directory}/swagger-schema</outputDirectory>
            <includes>**/*.json</includes>
          </artifactItem>
        </artifactItems>
      </configuration>
    </execution>
  </executions>
</plugin>
```

## Putting it all together

There are a lot of moving parts, so here it is all together:

- convert YAML files to JSON, using my custom Maven plugin
- unpack the shared JSON schema into the local filesystem, using the standard
  Maven dependency plugin
- validate the JSON files, using the Groupon Maven plugin

```xml
<!-- convert yaml to json in order to be able to apply JSON Schema validation -->
<plugin>
  <groupId>com.github.ngeor</groupId>
  <artifactId>yak4j-json-yaml-converter-maven-plugin</artifactId>
  <version>0.0.1</version>
  <configuration>
    <sourceDirectory>src/main/swagger</sourceDirectory>
    <includes>*.yml</includes>
    <outputDirectory>${project.build.directory}/swagger-as-json</outputDirectory>
  </configuration>
  <executions>
    <execution>
      <goals>
        <goal>yaml2json</goal>
      </goals>
      <phase>validate</phase>
    </execution>
  </executions>
</plugin>

<!-- unpack the swagger json schema from the shared artifact -->
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-dependency-plugin</artifactId>
  <version>3.1.1</version>
  <executions>
    <execution>
      <id>unpack</id>
      <phase>validate</phase>
      <goals>
        <goal>unpack</goal>
      </goals>
      <configuration>
        <artifactItems>
          <artifactItem>
            <groupId>com.acme</groupId>
            <artifactId>acme-swagger-schema</artifactId>
            <version>0.0.1</version>
            <type>jar</type>
            <outputDirectory>${project.build.directory}/swagger-schema</outputDirectory>
            <includes>**/*.json</includes>
          </artifactItem>
        </artifactItems>
      </configuration>
    </execution>
  </executions>
</plugin>

<plugin>
  <groupId>com.groupon.maven.plugin.json</groupId>
  <artifactId>json-schema-validator</artifactId>
  <version>1.2.0</version>
  <executions>
    <execution>
      <phase>validate</phase>
      <goals>
        <goal>validate</goal>
      </goals>
    </execution>
  </executions>
  <configuration>
    <validations>
      <validation>
        <directory>${project.build.directory}/swagger-as-json</directory>
        <jsonSchema>${project.build.directory}/swagger-schema/swagger.schema.json</jsonSchema>
        <includes>
          <include>swagger.json</include>
        </includes>
      </validation>
    </validations>
  </configuration>
</plugin>
```

## Conclusion

Validation and conventions belong in the CI. If you're developing RESTful
microservices with Swagger, it's important that you maintain the consistency of
the API across teams and services. Invest in automating these checks, for the
benefit of your API users.
