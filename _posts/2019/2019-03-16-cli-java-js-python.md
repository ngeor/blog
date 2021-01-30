---
layout: post
title: A CLI comparison of Java, JavaScript and Python
date: 2019-03-16
published: true
tags:
  - cli
  - java
  - javascript
  - python
---

The inspiration for this post is the
[Python, Ruby, and Golang: A Command-Line Application Comparison](https://realpython.com/python-ruby-and-golang-a-command-line-application-comparison/)
published on [Real Python](https://realpython.com/).

I've been sticking to my decision to [stop writing bash scripts] and it has paid
off. Python is great for small scripts and cli apps. I do have however some
older pet projects in JavaScript (nodeJS) which are a bit large to rewrite in a
single day. Additionally, most of the codebase at work is in Java, and context
switching can be difficult.

In any case, I thought it's a nice exercise to write down the common tasks a CLI
app has to do and how that can be done in these 3 programming languages.

## Command-Line Interface

What is expected from a cli? It should accept arguments in short form (e.g.
`-n`), long form (e.g. `--dry-run`). It should validate mandatory arguments and
it should provide a pretty help message of all the available options. Depending
on your needs, you might need sub-command style cli, like git offers.

### Java

The command line arguments are passed to the `main` method. I'm not aware of a
built-in CLI builder. With a quick search I found
[Apache Commons CLI](https://commons.apache.org/proper/commons-cli/), but I
haven't used it myself. It's
[usage page](https://commons.apache.org/proper/commons-cli/usage.html) has some
detailed examples.

### JavaScript (node.js)

Command line arguments are in `process.argv`. The array will start with
`['node', 'script.js']` and the CLI parameters will follow. I don't think
there's something in the standard library, but I've tried the [commander]
dependency, which works good enough.

### Python

Command line arguments are in `sys.argv`. The array will start with the script
`['script.py']` and the CLI parameters will follow. The standard library has
support for a rich parser in the [argparse] module.

## Environment variables

This is a no-brainer and it's supported out of the box everywhere:

- Java: `System.getenv("VARIABLE")`.
- JavaScript: `process.env.VARIABLE`
- Python: `os.environ['VARIABLE']`

A small problem with Java is that `System.getenv` is a static method and mocking
it for unit tests is not that easy.

## Recursively listing files (walking a directory)

### Java

This depends on the Java version you're targeting. Java 8 and later has a
simpler API:

```java
Files.walk(Paths.get("/tmp"))
  .filter(p -> p.getFileName().toString().endsWith(".txt"))
  .forEach(System.out::println);
```

In older versions, you might have to write the recursion yourself using the
`listFiles()` method of a `File` instance.

### JavaScript

node.js does not have a built-in function so you'd need to ~~write it yourself~~
[copy paste it from the internet](https://medium.com/@allenhwkim/nodejs-walk-directory-f30a2d8f038f):

```javascript
const fs = require("fs"),
  path = require("path");

function walkDir(dir, callback) {
  fs.readdirSync(dir).forEach(f => {
    let dirPath = path.join(dir, f);
    let isDirectory = fs.statSync(dirPath).isDirectory();
    isDirectory ? walkDir(dirPath, callback) : callback(path.join(dir, f));
  });
}
```

### Python

```python
for entry in os.walk('/tmp'):
  dirpath, dirnames, filenames = entry
```

For every directory, you get an `entry` which contains:

- `dirpath`: the path of the directory
- `dirnames`: an array of the sub-directories
- `filenames`: an array of the filenames on that directory

I like how Python already splits it into directories and files, which is what
you typically want.

## File reading / writing

### Java

In Java, it can get a bit verbose:

```java
try (
  BufferedReader bufferedReader = new BufferedReader(new FileReader("/tmp/test"));
  BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter("/tmp/test.copy"))
) {
  String line = bufferedReader.readLine();
  while (line != null) {
    bufferedWriter.write(line);
    bufferedWriter.newLine();
    line = bufferedReader.readLine();
  }
}
```

The library [Apache Commons IO] can help you out significantly:

```java
List<String> lines = FileUtils.readLines(new File("/tmp/test"), StandardCharsets.UTF_8);
FileUtils.writeLines(new File("/tmp/test.copy"), "utf8", lines);
```

### JavaScript

It's quite simple:

```js
const contents = fs.readFileSync("/tmp/test", "utf8");
fs.writeFileSync("/tmp/test.copy", contents, "utf8");
```

### Python

Slightly more verbose:

```python
with open('/tmp/test', encoding='utf8') as input_file:
  contents = input_file.read()
with open('/tmp/test.copy', 'w', encoding='utf8') as output_file:
  output_file.write(contents)
```

## Running a command

### Java

The `ProcessBuilder` class can help out:

```java
var processBuilder = new ProcessBuilder("git", "status")
  .directory(new File("/tmp"));

var process = processBuilder.start();
int exitCode = process.waitFor();
if (exitCode != 0) {
  // the command failed
}

// get the output of the command to process it
InputStream output = process.getOutputStream();
```

If we don't care to process the command's output, but we want to show it as part
of our cli app, then we can call
`redirectOutputStream(ProcessBuilder.Redirect.INHERIT)` on the `processBuilder`.

### JavaScript

nodeJS has the `child_process` module:

```js
const result = child_process.spawnSync("git", ["status"], {
  cwd: "/tmp",
  encoding: "utf8"
});
if (result.status) {
  // the command failed
}

// the output already as a string because of the `encoding` option
const output = result.stdout;
```

Similar with Java, there is a `stdio` option which by default is set to `pipe`
and it can be set to `inherit` if we just want the command's output to be shown
as if it were part of our own.

### Python

Python offers the `subprocess` module in the standard library:

```python
result = subprocess.run(['git', 'status'], cwd='/tmp')
if result.returncode != 0:
  // the command failed
```

Unlike the previous two, the default here is to print the output instead of
capture it.

To capture and process the output, we need to pass the `stdout=subprocess.PIPE`
option:

```python
result = subprocess.run(['git', 'status'], cwd='/tmp', encoding='utf8', stdout=subprocess.PIPE)
lines = result.stdout.splitlines()
```

A useful feature of Python is that it has a `check=True` option which will throw
an exception if the command didn't terminate with a zero exit code. This means
that you don't need to explicitly check if the `returncode` was zero after each
command.

## Reading / writing JSON

### Java

There are many libraries, I've used [Jackson]. Typically, you'd use it against a
pojo that you want to serialize/deserialize. It is possible to use it with a
map, although that wouldn't be the normal case in a strongly typed language like
Java:

```java
ObjectMapper objectMapper = new ObjectMapper();
Map<String, String> data = Map.of("hello", "world");

// serialize
String json = objectMapper.writeValueAsString(data);

// deserialize
Map<String, Object> value = objectMapper.readValue(
  json,
  new TypeReference<HashMap<String, Object>>() {}
);
```

But since the other two languages can serialize/deserialize maps, it's worth
showing that it's feasible also in Java.

### JavaScript

This works in node.js but also in the browser:

```js
JSON.stringify({ hello: "world" });
JSON.parse('{"hello":"world"}');
```

### Python

Python has support for JSON in the standard library `json` module:

```python
import json
json.dumps({ 'hello': 'world' })
json.loads('{"hello":"world"}')
```

## Calling an HTTP API

### Java

Java 11 has a
[new HTTP Client](https://openjdk.java.net/groups/net/httpclient/intro.html). I
didn't even know about it until 5 minutes ago. I gave it a try and it works on
my machine:

```java
HttpClient httpClient = HttpClient.newHttpClient();
HttpRequest httpRequest = HttpRequest.newBuilder(URI.create("https://api.bitbucket.org/2.0/repositories/"))
        .version(HttpClient.Version.HTTP_1_1)
        .GET()
        .build();
HttpResponse<String> httpResponse = httpClient.send(httpRequest, HttpResponse.BodyHandlers.ofString());
System.out.println(httpResponse.body());
```

For external dependencies, if you're already using Spring, you should probably
use the Spring Rest Template. The [OkHttp] client is also nice and it supports
Android too.

### JavaScript

The standard `https` module reminds me why I don't like asynchronous programming
in node.js:

```js
const req = https.request(url, requestOptions, res => {
  const minSuccess = 200;
  const maxSuccess = 300;
  let message = "";
  if (res.statusCode >= minSuccess && res.statusCode < maxSuccess) {
    res.on("data", chunk => {
      message += chunk;
    });

    res.on("end", () => {
      // at this point we have the payload in message
    });
  } else {
    res.on("data", d => {
      process.stdout.write(d);
    });

    // oops error
  }
});

req.end();

req.on("error", e => {
  // oops different error
});
```

The [request](https://www.npmjs.com/package/request) external dependency tries
to make things prettier. If you want to use Promises and `async/await`, you have
(at least) 3 alternative extra libraries to pick from (which is why I often feel
this is a prank).

### Python

The standard library has the `urllib.request` module which is okay:

```python
req = urllib.request.Request(url, headers={
  'Authorization': 'Basic super-secret-credentials-in-base64'
})

with urllib.request.urlopen(req) as response:
  json_response = json.load(response)
```

or if you want to post some data:

```python
payload = json.dumps({
  'hello': 'world'
}).encode('utf8')

req = urllib.request.Request(url, data=payload, method='POST', headers={
  'Authorization': 'Basic again-it-is-a-secret',
  'Content-Type': 'application/json'
})

with urllib.request.urlopen(req) as response:
  status = response.status
  if status < 200 or status >= 300:
    raise ValueError(f'Oops: {status}')
```

Even the
[documentation of urllib.request](https://docs.python.org/3/library/urllib.request.html)
mentions that the external dependency [Requests package] is recommended for a
higher-level HTTP client interface. I've tried it also, and it is kind of
better, but I think that the default is not too bad (and having worked enough
with npm I don't like adding too many dependencies).

## Distribution

How will the users install your app?

### Java

To the best of my knowledge, this is missing in the Java world.

### JavaScript

You can publish your app on the npm registry. The users can then install it with
npm.

e.g. `npm i -g eslint` will install the `eslint` cli.

A great feature of npm is the npx variant which allows you to run an app without
installing it, e.g. `npx eslint` will install `eslint` temporarily, run it, and
remove it. It is quite fast too.

### Python

Similar with npm, you have pip. You can publish your app on the PyPI registry
and the users can install it with pip.

A minor difference for Windows: npm generates cmd scripts while pip generates
exe stubs.

## Overall remarks

### Java

Both the language and the standard library show their age. While the standard
library has support for XML and zip files, it doesn't have built-in support for
JSON. The need for backwards compatibility means that there are multiple ways of
doing the same thing (e.g. `java.time`, `java.nio`, `List.of`, etc). The
programming style is often a bit verbose. Checked exceptions can be annoying
(I've omitted them from all examples) and don't play well with newer language
features like lambdas and streams.

### JavaScript/node.js

The standard library is async-first, designed for high performing non-blocking
services. This is something of little value for small cli apps. The language
itself has 3 different ways of doing async operations (callback hell, promises,
async/await), which doesn't make things easier. All in all, it's not bad to be
honest. I deliberately used synchronous variants in the above examples whenever
possible.

### Python

The standard library can get you very far without having to install any external
dependency. There are options that take into account common use cases, such as
validate the success of an external command, which adds extra appreciation
points for usability in my book, that feeling that someone went for the extra
mile.

## Conclusion

[De gustibus et coloribus non est disputandum](https://en.wiktionary.org/wiki/de_gustibus_et_coloribus_non_est_disputandum).
Pick whatever you like. I like to write less code and having less dependencies
to worry about. And remember that
[there are two kinds of programming languages: the ones people complain about and the ones that nobody uses](https://en.wikiquote.org/wiki/Bjarne_Stroustrup).

[stop writing bash scripts]: {% post_url 2019/2019-02-11-goodbye-bash %}
[commander]: https://www.npmjs.com/package/commander
[argparse]: https://docs.python.org/3/library/argparse.html
[Apache Commons IO]: https://commons.apache.org/proper/commons-io/
[Jackson]: https://github.com/FasterXML/jackson
[OkHttp]: https://square.github.io/okhttp/
[Requests package]: http://docs.python-requests.org/en/master/
