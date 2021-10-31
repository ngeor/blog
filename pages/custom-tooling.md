---
layout: page
title: Custom Tooling
date: 2021-10-31
---

A catalog of custom tooling I've written. yak4j stands for [yak shaving] for
Java.

## Batch processing

- [instarepo] applies batch changes to multiple repositories.

## Scaffolding

- [archetype-quickstart-jdk8] Maven archetype

## Getting latest

- [yak4j-sync-archetype-maven-plugin] Regenerates a project out of its maven
  archetype and overwrites specific files

## Versioning

- [yart] helps with releasing a project that follows semantic versioning

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

[archetype-quickstart-jdk8]: https://github.com/ngeor/archetype-quickstart-jdk8
[checkstyle-rules]: https://github.com/ngeor/checkstyle-rules
[instarepo]: https://github.com/ngeor/instarepo
[yak4j-filename-conventions-maven-plugin]: https://github.com/ngeor/yak4j-filename-conventions-maven-plugin
[yak4j-json-yaml-converter-maven-plugin]: https://github.com/ngeor/yak4j-json-yaml-converter-maven-plugin
[yak4j-spring-test-utils]: https://github.com/ngeor/yak4j-spring-test-utils
[yak4j-swagger-maven-plugin]: https://github.com/ngeor/yak4j-swagger-maven-plugin
[yak4j-sync-archetype-maven-plugin]: https://github.com/ngeor/yak4j-sync-archetype-maven-plugin
[yak4j-utc-time-zone-mapper]: https://github.com/ngeor/yak4j-utc-time-zone-mapper
[yak4j-xml]: https://github.com/ngeor/yak4j-xml
[yart]: https://github.com/ngeor/yart
[yak shaving]: https://en.wiktionary.org/wiki/yak_shaving
