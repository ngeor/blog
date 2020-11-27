---
layout: post
title: Dropwizard with Immutables
date: 2020-10-11 14:19:06 +02:00
tags:
  - java
  - dropwizard
  - immutables
---

In this post, I'm using [Dropwizard](https://www.dropwizard.io/en/latest/)
together with the [Immutables](https://immutables.github.io/) library and
sharing some thoughts on OOP.

Dropwizard is a Java framework for developing RESTful web services. I've been
using it at work for almost a year now. It's not a mega framework like Spring,
but it gets the job done.

Immutables is a Java library for creating immutable value objects.

Let's imagine we have a Dropwizard resource that deals with books and has two
methods: one for returning a list of books and one for adding a new book:

```java
@GET
public List<Book> getBooks() {
  // get the books
}

@POST
public Response addBook(@NotNull @Valid Book book) {
  // add a book
}
```

The most common way of implementing `Book` is to create a POJO class, with its
getters and setters, in 20 lines of traditionally verbose Java code:

```java
public class Book {
  private String isbn;
  private String title;

  public String getIsbn() {
    return isbn;
  }

  public void setIsbn(String isbn) {
    this.isbn = isbn;
  }

  public String getTitle() {
    return title;
  }

  public void setTitle(String title) {
    this.title = title;
  }
}
```

You could also skip the getters and setters and go for public fields:

```java
public class Book {
  public String isbn;
  public String title;
}
```

In OOP, the above is frowned upon (and that's putting it mildly). Exposing
public fields is a violation of one of the basic principles of OOP. So why would
you go for this?

In my mind, OOP design is about classes that have state and behaviour (fields
and methods). That's all totally valid. But, when you're programming methods
that receive or return JSON objects, these classes are supposed to be nothing
more than that. I think the fact that Java is adding
[records](https://blogs.oracle.com/javamagazine/records-come-to-java)
([C# too by the way](https://devblogs.microsoft.com/dotnet/welcome-to-c-9-0/#records))
is a recognition to the fact that data transfer objects deserve to have a
first-class support without having to write unnecessary boilerplate just to
avoid the stigma of the heretic.

When I think of practices like immutability, or favoring composition over
inheritance, I wonder if perhaps there ought to be a book "OOP - the good
parts".

Back to the Immutables library: I like to use Immutables instead of the two
above approaches (especially when it comes to responses):

```java
@Value.Immutable
@JsonSerialize(as = ImmutableBook.class)
@JsonDeserialize(as = ImmutableBook.class)
public interface Book {
  String getIsbn();

  String getTitle();
}
```

Validation works as expected (e.g. let's demand that both ISBN and title are not
blank):

```java
public interface Book {
  @NotBlank
  String getIsbn();

  @NotBlank
  String getTitle();
}
```

Caveat: it only works when using getter style methods. It is not unusual for
Immutables to use a different naming convention for the methods like
`String isbn()`. In that case, validation doesn't work.

Creating the responses is done with a builder object:

```java
public List<Book> getBooks() {
  return List.of(
    ImmutableBook.builder()
      .isbn("978-0078817038")
      .title("Turbo PASCAL 6: The Complete Reference (Programming series)")
      .build()
  );
}
```

I personally like this approach more, especially because of the builder object.
