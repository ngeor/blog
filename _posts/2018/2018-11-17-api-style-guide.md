---
layout: post
title: API Style Guide
date: 2018-11-17
published: true
categories:
- tech
tags:
- rest
- swagger
- microservices
- notes
---

Using a microservice architecture allows development teams to work separately,
delivering work faster and focusing on a specific part of the business domain.
Working independently means that developers are free to make their own choices.
While that's great, there's the risk of building the tower of Babel.

Imagine this simple example: team A is developing an address book service,
team B is working on an invoice service. The first team is using Java, the
second is using .NET. They both follow the default options for their stack.
When we put service A and B together, we'll have an address book API which uses
camelCase for the payload of the requests, while the invoice service uses
PascalCase. Technically it works, but it looks unprofessional and it will be
difficult to integrate with.

We need an **API style guide** to ensure that the API looks consistent. It's the
same as using a code style guide to ensure that the code looks as if it was
written by one person.

In this post, I'm describing the conventions we currently use at work. This is
all about a RESTful design, influenced a bit by the fact that we use Swagger and
Java / Spring Boot. And just like code style guide, it's all a bit subjective.
It's more important to follow a specific set of rules rather than arguing about
tabs vs spaces, lowercase vs uppercase, etc.

## URL Conventions

### Path Conventions

The URL is the endpoint to a single resource (HTTP, RESTful) or operation (HTTP,
RPC style).

Example of a URL that identifies uniquely a shipment:

- https://api.acme.com/v1/shipping/shipments/42

Example of a URL that maps to an operation:

- https://api.acme.com/v1/auth/availability

We favour RESTful design, but sometimes RPC is more natural.

In any case, the naming conventions for the URLs are:

- no spaces or special characters
- only lowercase
- separate words with hyphens (e.g. `address-book`. Not `addressbook` or
  `address_book`).

### Query String Parameters Conventions

- no spaces or special characters
- only lowercase
- separate words with underscores (e.g. `per_page` . Not `perpage`, `perPage`,
  or `per-page`).

### Payload Conventions

The body of the request is a JSON object. All properties need to use camelCase,
which is the default for Java and JavaScript (.NET by default is using
PascalCase).

Example:

```json
{
  "firstName": "Tom",
  "lastName": "Jones"
}
```

### Enums

Enums can appear in the body of a request, as well as in the query string as
parameters. We use FULL_CAPS for enums, because it makes the generated Java code
easier to understand.

Examples: `ASC`, `DESC`, `EXPRESS_DELIVERY`.

## Swagger Conventions

### Operation IDs

All operation identifiers are camelCase e.g. `createAddress`.

This matches the convention for Java method names. This is reflected in the
generated code but also in the documentation.

### Definitions

All definitions (model names) are PascalCase e.g. `Shipment`, `PriceResult`.

This matches the convention for Java class names and it is reflected in the
generated code and documentation.

### Documentation

All elements need to have a description. The description will be published in
the documentation so it needs to be helpful and in proper English.

### Tags

All operations need to be assigned to a tag. Tags have an impact on the
documentation but also on the generated client SDKs. If you don't use a tag,
they get grouped in the "Default" tag, which is most likely not what you want.

Example:

```yaml
paths:
  /addresses:
    get:
      operationId: getAddresses
      tags:
      - AddressBook
```

The naming convention for tags is PascalCase.

### (Optional) Example values

It is possible to define example values explicitly with the example property:

```yaml
firstName:
  type: string
  description: The first name of a person
  example: John
```

This can be useful in the documentation, but it is not required.

### Hide the type of identifiers

Sometimes we use numeric identifiers (e.g. entities coming from PostgreSQL).
Sometimes we use GUIDs. Sometimes identifiers are strings.

The caller of the API should not care about our identifiers. It should all be
just a string. This has some benefits:

- hides the details of our implementation
- allows us to change the underlying storage to even a different ID type without
  changing the API security through obscurity

Example:

```yaml
Address:
  properties:
    id:
      type: string
```

```json
{
  "id": "42"
}
```

## REST Conventions

### Response Codes

We use the appropriate status codes in the response.

- 2xx indicates a success
- 4xx indicates a client error
- 5xx indicates a server error

More specifically:

- 200 indicates a success
- 201 (CREATED) indicates that a new entity was created. This should be used as
  the response to a POST operation which created a new entity.
- 400 indicates a validation error
- 401 indicates that the user is not properly authenticated (missing or bad
  authentication)
- 403 indicates that the user is authenticated but is not authorized to access
  the resource or perform the requested action
- 404 indicates that the requested resource is not found
- 405 Method not allowed (e.g. GET instead of POST)
- 406 Not acceptable (content type is not accepted)
- 409 (CONFLICT) indicates that an entity already exists

See [here for 401 vs 403](https://stackoverflow.com/questions/3297048/403-forbidden-vs-401-unauthorized-http-responses).

### Which response codes should be documented?

You should document only the response codes that add some value to the user of
the API. We assume that the user of the API understands the difference between a
client error (4xx) and a server error (5xx). It is not our intention to
re-document the HTTP protocol.

Example:

200 - User added to role successfully.

Example of redundant documentation:

400 - Invalid request. This can be due to missing or invalid fields.

### Errors

We use the same object for reporting errors in all services. It is modelled
after Spring's exception so that we have the same data model for exceptions
coming from our code as well as exceptions coming from Spring itself (e.g.
validation errors are handled by Spring).

The object is defined in the source code like this:

```yaml
ErrorInfo:
  type: "object"
  description: "An error thrown by the API"
  properties:
    timestamp:
      type: "string"
      description: "The date-time when the error occurred"
    status:
      type: "number"
      format: "int32"
      description: "The status code of the error"
    error:
      type: "string"
      description: "The type of the error"
    message:
      type: "string"
      description: "A message describing the error"
    path:
      type: "string"
      description: "The URL path where the error occurred"
    errors:
      type: "array"
      description: "A collection of details about the errors"
      items:
        $ref: "#/definitions/ErrorDetail"
ErrorDetail:
  type: "object"
  description: "Details about an error, usually specific to a field."
  properties:
    defaultMessage:
      type: "string"
      description: "A detailed error message"
    objectName:
      type: "string"
      description: "The name of the object that caused the error"
    code:
      type: "string"
      description: "A code for the specific error"
```

### HTTP Verbs

We use the appropriate HTTP verb per operation.

| Verb   | Typical Use Case            |
|--------|-----------------------------|
| GET    | Get a resource              |
| POST   | Create a new resource       |
| PUT    | Update an existing resource |
| DELETE | Delete an existing resource |

Typically it is expected that calling a GET operation multiple times does not
create side-effects.

## CRUD Conventions

Several services define a set of CRUD (create, read, update, delete) operations
on a resource. Let's see an example for the address book:

| Operation Id  | HTTP Verb | HTTP Path              | HTTP Parameters                   | Payload |
|---------------|-----------|------------------------|-----------------------------------|---------|
| getAddresses  | GET       | /addresses             | Searching, Sorting and Pagination | -       |
| createAddress | POST      | /addresses             | -                                 | Address |
| updateAddress | PUT       | /addresses             | -                                 | Address |
| getAddress    | GET       | /addresses/{addressId} | -                                 | -       |
| deleteAddress | DELETE    | /addresses/{addressId} | -                                 | -       |

Points of interest:

- the HTTP path uses the plural form addresses and not the singular address
- the operation IDs are prefixed with get, create, update and delete
- the HTTP path for a single address is a sub-path under the main path e.g.
  /addresses/42

## Searching, Sorting and Pagination

When getting a list of objects, we typically want to limit the number of
results, apply some sorting, and filter for something specifically.

### Searching

This refers to free text search on one or more fields.

Each operation needs to document which fields are being taken into account.

We use the `q` parameter for this type of search.

Examples:

- /addresses?q=Tom
- /addresses?q=1017
- /users?q=Leo

### Sorting

Our conventions are based on [GitHub conventions](https://developer.github.com/v3/repos/).

- the field to sort by is defined by the `sort` parameter. The valid values for
  this parameter depend on the object. The value should use camelCase, just like
  the field names being sorted. In the advanced case of nesting, use a dot to
  separate fields.
- the sorting direction is defined by the `direction` parameter. As this is an
  enum, the value needs to be in FULL_CAPS. The valid values are `ASC` and
  `DESC`.

Examples:

- /addresses?sort=firstName
- /addresses?sort=lastName&direction=DESC
- /shipments?sort=sender.company&direction=ASC

The direction parameter should be optional and the default value should be
documented per operation.

### Pagination

We follow [GitHub's API regarding pagination](https://developer.github.com/v3/#pagination).

- current page is defined by the `page` parameter
- page numbering is one-based, not zero-based
- omitting the page parameter will return the first page
- the page size is defined by the `per_page` parameter
- omitting the `per_page` parameter will return a sensible default per
  operation, which should be documented

Examples:

- /addresses (fetches the first 10 results according to the default sorting rules)
- /addresses?page=2 (fetches the next 10 results)
- /addresses?page=3&per_page=20 (fetches addresses 41-60)
