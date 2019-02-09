---
layout: post
title: Merging Swagger files
date: 2018-10-28
published: true
categories:
- ci-tooling
tags:
- swagger
- java
- maven
- plugin
- microservices
- api gateway
- ci-tooling
---

Consider the following scenario. You have a few microservices and they're all
developed independently: they don't share code, they don't share data and they
don't share schema. They're all exposing their own REST API. To make things a
bit simple, their API is defined in a swagger file.

Now, you want to give your API to a client who wants to integrate with your
platform. It would be easy for you to give out each microservice's API and
documentation. However, it wouldn't be very easy for the person who wants to
integrate with you. Ideally, he/she would prefer to receive a single endpoint to
call.

Implementing this _API Gateway_ type of endpoint is not very difficult. You just
need to deploy a reverse proxy (e.g. nginx) which will route traffic to the
microservices. Let's see an example:

| Service  | Endpoint                       |
|----------|--------------------------------|
| Products | https://**products.**acme.com/ |
| Orders   | https://**orders.**acme.com/   |

With the reverse proxy available at https://api.acme.com/ we get this mapping:

| Service  | Endpoint                               |
|----------|----------------------------------------|
| Products | https://**api.**acme.com/**products**/ |
| Orders   | https://**api.**acme.com/**orders**/   |

The implementation under the hood is still using microservices, but now it's a
bit easier for the client to use the API. Being an extra level of indirection,
it offers some advantages to us as well. You can swap the implementation of a
service with a different one without breaking the client's integration for
instance. You have a single point to implement SSL termination and CORS. It
opens up possibilities.

There's one small problem left. The documentation of the API. Since the
microservices are using Swagger, the documentation is automatically generated.
However, now we have a slightly different API (e.g. we have paths like
`/products/` and `/orders/` which our microservices know nothing about).

We can create a composite swagger file, combining the swagger files of the
microservices. That will allow us to generate the documentation automatically
again. It is however difficult to do manually.

First of all, you'll need to prefix all paths with the correct prefix. That's
easy, albeit boring and error prone.

The real challenge is the model definitions. If you're lucky, all services
have different model names. As each microservice is independently developed
and captures its own view of the domain, it is not uncommon that the same
model name exists in multiple services. The semantics might differ from domain
to domain, so it is possible that you have the same model with different
definition in each service.

In our example, the Products service might have a Product model which has
fields like Title, Color, Size, WashingInstructions. The Orders service on the
other hand might also have a Product model but with fields like Title and
RetailPrice.

You'll probably need to rename the models, maybe prefix them with the service
name, before you add them to the composite swagger file. And, of course,
rename all references of these models wherever they're used.

That's a lot of work. And you will need to do it everytime the API of a service
changes.

As it turns out, I had to perform this task, and I'm not a fan of doing things
manually. That's why I created a [swagger maven
plugin](https://github.com/ngeor/yak4j/tree/master/yak4j-swagger-maven-plugin)
which does these tasks automatically.

Here's how it can be used in order to merge the swagger files, applying
prefixes to paths and model definitions:

```xml
<plugin>
  <groupId>com.github.ngeor</groupId>
  <artifactId>yak4j-swagger-maven-plugin</artifactId>
  <version>${yak4j.version}</version>
  <executions>
    <execution>
      <id>merge</id>
      <goals>
        <goal>merge</goal>
      </goals>
      <configuration>
        <inputs>
          <input>
            <file>src/main/swagger/products.yml</file>
            <pathPrefix>/products</pathPrefix>
            <definitionPrefix>Products</definitionPrefix>
          </input>
          <input>
            <file>src/main/swagger/orders.yml</file>
            <pathPrefix>/orders</pathPrefix>
            <definitionPrefix>Orders</definitionPrefix>
          </input>
        </inputs>
        <output>${project.build.directory}/composite.yml</output>
      </configuration>
    </execution>
  </executions>
</plugin>
```

I run this plugin just before I run the standard swagger generator maven plugin
and I get the composite documentation for my API for free.

Hope this helps.
