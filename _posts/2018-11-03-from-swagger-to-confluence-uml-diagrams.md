---
layout: post
title: From Swagger to Confluence UML diagrams
date: 2018-11-03
published: true
categories:
- Code
tags:
- Swagger
- Confluence Cloud
- automation
- UML
- Docker
author: Nikolaos Georgiou
---

TL;DR: During CI, I am generating a UML diagram out of the Swagger definition
and I'm publishing it to Confluence.

At work we use Swagger to define our REST APIs. With the [swagger codegen maven
plugin], we can generate a lot of code (models and interfaces for the
controllers) as well as our API documentation. But a picture is worth a thousand
words, so I wanted a way to automatically generate a UML diagram out of the
Swagger definition.

With a little bit of investigation, I found [Swagger to UML]. It's a small
script written in Python which converts the Swagger definition into [Plant UML]
diagrams. Plant UML then renders the diagram into PNG or SVG but it requires
[Graphviz] to be installed.

There are a lot of moving parts here with various technologies. Swagger to UML
needs Python. Plant UML needs Java and Graphviz. And I would like all these to
run automatically during CI. [Sounds like it's time to bake a Docker
image!](https://xkcd.com/1988/)

I created the [swagger-to-diagram] Docker image which assembles together:

- JRE 11
- Python 3
- Swagger to UML
- Plant UML
- Graphviz
- a custom bash script to execute the above

With that Docker image in place, I can generate my PNG diagram like this:

```
docker run --rm -v $PWD:/data \
  ngeor/swagger-to-diagram swagger2png.sh \
  ./src/main/swagger/swagger.yml diagram.png
```

In Bitbucket Pipelines, that's just an extra step definition:

```yml
step:
  name: Generate UML diagram from Swagger file
  image: ngeor/swagger-to-diagram
  script:
  - swagger2png.sh ./src/main/swagger/swagger.yml diagram.png
```

And now, for the cherry on the top: I also added a script which publishes the
PNG diagram as an attachment to Confluence Cloud. That's the extra mile that
makes the whole process more magic. And it's just a `curl` call to the
Confluence Cloud REST API which [creates or updates
attachments](https://developer.atlassian.com/cloud/confluence/rest/#api-content-id-child-attachment-put).

The script is packaged in the same Docker image and you can call it like this:

```
put-confluence-attachment.sh -u $USERNAME:$PASSWORD \
  --domain acme \
  --content-id $CONFLUENCE_CONTENT_ID \
  --comment "Attaching UML diagram" \
  --filename diagram.png
```

You'll need a Confluence Cloud instance at `https://acme.atlassian.net/wiki`
(that's the `domain` parameter) as well as a username and password to access the
REST API. You'll also need a page to attach the diagram to. That's the
`content-id` parameter.

In my case, I have one Confluence page per microservice. When the build of a
microservice succeeds, it updates the diagram on the microservice's page.

Some practical tips:

1. Don't use your personal Confluence credentials. Instead, create a dedicated
   account for automations like these. This way you can control better the
   access rights of the account. Plus, it looks much more awesome to see that a
   page was changed by a bot.
2. Store the Confluence credentials as global environment variables in your CI
   server, so that you don't have to repeat them on each project.
3. If you use a different Confluence page per project (that's what I do), then
   you should store that page's ID as a project environment variable in your CI
   server. You could however use a single page and just use a different filename
   per diagram.

In the end, you get a fancy diagram in Confluence:

<figure><img src="{{ site.baseurl }}/assets/2018/11/uml-confluence.png" /><figcaption>From Swagger to Confluence</figcaption></figure>


[swagger codegen maven plugin]: https://github.com/swagger-api/swagger-codegen/tree/master/modules/swagger-codegen-maven-plugin
[Swagger to UML]: https://github.com/nlohmann/swagger_to_uml
[Plant UML]: http://plantuml.com/
[Graphviz]: http://www.graphviz.org/
[swagger-to-diagram]: https://github.com/ngeor/docker-swagger-to-diagram
