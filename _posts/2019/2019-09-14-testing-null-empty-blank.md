---
layout: post
title: Testing null, empty, blank
date: 2019-09-14
published: true
tags:
  - java
  - junit5
  - unit tests
---

In many cases, when you have a method that accepts a mandatory string parameter,
you want to verify that the parameter contains a value that isn't `null`, nor
empty, not blank (i.e. consisting solely of whitespace characters). While
writing the check is easy, testing it can be a bit annoying.

Let's see an example of such a method:

```java
class Greeter {
  public void greet(String person) {
    if (person == null || person.isBlank()) {
      throw new IllegalArgumentException("person is mandatory");
    }

    System.out.println("Hello " + person);
  }
}
```

By the way, if you're already using
[Apache Commons](https://commons.apache.org/), you can replace the `if` block
with a call to
[Validate.notBlank](<https://commons.apache.org/proper/commons-lang/javadocs/api-3.1/org/apache/commons/lang3/Validate.html#notBlank(T)>).
But let's see how we can test this.

## Take 1

The most straightforward way is to write three separate unit tests:

```java
@Test
void nullIsNotAllowed() {
  assertThatThrownBy(() -> greet(null))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessage("person is mandatory");
}

@Test
void emptyIsNotAllowed() {
  assertThatThrownBy(() -> greet(""))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessage("person is mandatory");
}

@Test
void blankIsNotAllowed() {
  assertThatThrownBy(() -> greet(" "))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessage("person is mandatory");
}
```

This works fine, but it's repetitive and difficult to manage.

## Take 2

We can use parameterized tests to trim it down a bit:

```java
@Test
void nullIsNotAllowed() {
  assertThatThrownBy(() -> greet(null))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessage("person is mandatory");
}

@ParameterizedTest
@ValueSource(strings = {
  "",
  " "
})
void emptyAndBlankAreNotAllowed(String person) {
  assertThatThrownBy(() -> greet(person))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessage("person is mandatory");
}
```

Unfortunately, we can't get rid of the `null` test, because it's not possible to
assign a `null` to the `strings` property of the `@ValueSource` annotation. It
would be great if jUnit allowed some property like `includeNull = true` in the
annotation in order to cover this scenario.

## Take 3

But, there are still ways to go. The `CsvSource` is a nice option, if a bit
obscure:

```java
@ParameterizedTest
@CsvSource({
  ",",      // null
  "''",     // empty
  "' '"     // blank
})
void invalidValuesAreNotAllowed(String person) {
  assertThatThrownBy(() -> greet(person))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessage("person is mandatory");
}
```

With this trick, we catch all cases in a single test method:

- `,` represents a CSV row where we skip the first column with a comma. This
  generates a `null` value for the test. It's not very straightforward but it
  works.
- `''` is an empty string.
- `' '` is a blank string.

We have trimmed it down to one test method, which is great. The strings we're
using might be a bit cryptic though and we have to copy paste them around.

## Take 4

We can use a static method to generate the values instead:

```java
private static String[] nullEmptyBlankSource() {
  return new String[] { null, "", " " };
}

@ParameterizedTest
@MethodSource("nullEmptyBlankSource")
void invalidValuesAreNotAllowed(String person) {
  assertThatThrownBy(() -> greet(person))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessage("person is mandatory");
}
```

And we can move the static method to a separate class, so that it can be reused
in multiple tests:

```java
public final class TestUtil {
  private TestUtil() {}

  public static String[] nullEmptyBlankSource() {
    return new String[] { null, "", " " };
  }
}

class GreeterTest {
  @ParameterizedTest
  @MethodSource("com.acme.example.TestUtil#nullEmptyBlankSource")
  void invalidValuesAreNotAllowed(String person) {
    assertThatThrownBy(() -> greet(person))
      .isInstanceOf(IllegalArgumentException.class)
      .hasMessage("person is mandatory");
  }
}
```

The only problem here is that the method is defined as a string, which means you
lose the compile-time safety. If you rename the method or the class that the
`MethodSource` points to, you won't get a compilation error.

## Take 5

A next step can be to define our own custom annotation as a source of
parameterized tests:

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@ArgumentsSource(BlankStringProvider.class)
@interface BlankStringSource {

}

class BlankStringProvider implements ArgumentsProvider, AnnotationConsumer<BlankStringSource> {

  @Override
  public void accept(BlankStringSource blankStringSource) {

  }

  @Override
  public Stream<? extends Arguments> provideArguments(ExtensionContext context) throws Exception {
    return Stream.of(
      Arguments.of((String) null),
      Arguments.of(""),
      Arguments.of(" ")
    );
  }
}

@ParameterizedTest
@BlankStringSource
void invalidValuesAreNotAllowed(String person) {
  assertThatThrownBy(() -> greet(person))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessage("person is mandatory");
}
```

Now we have a bit more (reusable) code to write, but we end up with a
parameterized test that just needs a simple annotation, `@BlankStringSource`, in
order to cover our edge cases.

## Update: Take 6

Many thanks to [Sam Brannen](https://twitter.com/sam_brannen) who brought
[this solution](https://twitter.com/sam_brannen/status/1172784780750073856) to
my attention!

So, today I learned:

- it's possible to combine multiple sources on a parameterized test
- there is a built-in `NullSource` which provides a `null` argument
- there is a built-in `EmptySource` which provides an empty argument
- and a composite `NullAndEmptySource` which provides both
- the
  [documentation](https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests-sources-null-and-empty)
  already covers the null, empty and blank scenario (because RTFM)

With all that in mind, here's another take on the solution:

```java
@ParameterizedTest
@NullAndEmptySource
@ValueSource(strings = " ")
void invalidValuesAreNotAllowed(String person) {
  assertThatThrownBy(() -> greet(person))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessage("person is mandatory");
}
```
