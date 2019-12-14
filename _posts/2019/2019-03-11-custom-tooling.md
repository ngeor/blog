---
layout: page
title: Custom Tooling
date: 2019-03-11
categories:
  - pet-projects
---

A catalog of custom tooling I've written. yak4j stands for [yak shaving] for
Java.

## Creating a new project

- [instarepo] creates a new git repository and activates build pipeline

### Scaffolding

- [archetype-quickstart-jdk8] Maven archetype
- [generator-csharp-cli-app] Yeoman generator for a C# cli app
- [generator-csharp-nuget-lib] Yeoman generator for a C# NuGet package
- [generator-nodejs] Yeoman generator for a nodeJS app

## Getting latest

- [clone-all] clones all missing repositories from GitHub or Bitbucket Cloud
- [dirloop] runs the same command over multiple directories (e.g.
  `dirloop git pull`)
- [yak4j-sync-archetype-maven-plugin] Regenerates a project out of its maven
  archetype and overwrites specific files

## Versioning

- [yak4j-bitbucket-maven-plugin] breaks the build if the tag already exists,
  creates a tag on successful build
- [yart] manual bump version and tag publishing

## Linting

- [checkstyle-rules] custom checkstyle rules
- [yak4j-filename-conventions-maven-plugin] ensures filenames follow a naming
  convention

## Code generation

- [yak4j-swagger-maven-plugin] Merges multiple swagger files into one
- [yak4j-json-yaml-converter-maven-plugin] Converts between JSON and YAML files

## Code libraries

- [yak4j-xml] friendlier wrapper around JAXB which throws unchecked exceptions
- [yak4j-utc-time-zone-mapper] mapper between LocalDateTime and OffsetDateTime,
  can be used together with MapStruct

## Testing libraries

- [yak4j-spring-test-utils] custom assertJ assertions for Spring
  TestRestTemplate and MvcActions

## Docker Images

I moved all my custom Docker images in a single repository: [dockerfiles].
Includes images regarding:

- Deployment with helm, kubectl, terraform
- nodeJS with headless Chrome
- Generate diagrams out of swagger definitions and publish them to Confluence
  Cloud

[archetype-quickstart-jdk8]: https://github.com/ngeor/archetype-quickstart-jdk8
[checkstyle-rules]: https://github.com/ngeor/checkstyle-rules
[clone-all]: https://github.com/ngeor/clone-all
[dirloop]: https://github.com/ngeor/dirloop
[dockerfiles]: https://github.com/ngeor/dockerfiles
[generator-csharp-cli-app]: https://github.com/ngeor/generator-csharp-cli-app
[generator-csharp-nuget-lib]:
  https://github.com/ngeor/generator-csharp-nuget-lib
[generator-nodejs]: https://github.com/ngeor/generator-nodejs
[instarepo]: https://github.com/ngeor/instarepo
[yak4j-bitbucket-maven-plugin]:
  https://github.com/ngeor/yak4j-bitbucket-maven-plugin
[yak4j-filename-conventions-maven-plugin]:
  https://github.com/ngeor/yak4j-filename-conventions-maven-plugin
[yak4j-json-yaml-converter-maven-plugin]:
  https://github.com/ngeor/yak4j-json-yaml-converter-maven-plugin
[yak4j-spring-test-utils]: https://github.com/ngeor/yak4j-spring-test-utils
[yak4j-swagger-maven-plugin]:
  https://github.com/ngeor/yak4j-swagger-maven-plugin
[yak4j-sync-archetype-maven-plugin]:
  https://github.com/ngeor/yak4j-sync-archetype-maven-plugin
[yak4j-utc-time-zone-mapper]:
  https://github.com/ngeor/yak4j-utc-time-zone-mapper
[yak4j-xml]: https://github.com/ngeor/yak4j-xml
[yart]: https://github.com/ngeor/yart
[yak shaving]: https://en.wiktionary.org/wiki/yak_shaving
