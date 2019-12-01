---
layout: post
title: Debugging Docker with IntelliJ IDEA
date: 2017-03-26 07:08:27.000000000 +02:00
published: true
categories:
- programming
tags:
- Docker
- IntelliJ IDEA
- Java
- Kafka
- maven
---

In this post we'll create a small Java application, run it inside a Docker
container, and use IntelliJ IDEA to debug. This is a rather large post, so take
your time.

<h3>Introduction to the app</h3>

First, an introduction to the application itself. I started this as an
experiment for Kafka and <a href="https://avro.apache.org/"
target="_blank">Apache Avro</a>. There are two main classes in the application:
a producer and a consumer. They can be started individually and the producer is
able to send sample "users" to the consumer. A user is an object that has a
name, a favorite number and a favorite color. The producer is interactive, so
you type at the console the user's information and the user gets published to
Kafka, serialized with Avro. The consumer simply polls forever, printing any
user it might receive. We'll package the consumer into a Docker image.

The overall picture looks something like this:

<img src="{{ site.baseurl }}/assets/2017/avro.png" />

but we'll focus on the Docker side and debugging with IntelliJ.

<h3>Creating a Docker image</h3>

To create a Docker image, we need a Dockerfile. It looks like this:

```dockerfile
FROM openjdk:8-jre

# change directory to where the app will live
WORKDIR /usr/local/playground/

# install the jars
COPY target/*.jar ./

CMD ["java", "-cp", "kafka-playground-1.0-SNAPSHOT.jar:*", "ngeor.UserConsumer"]
```

Lines starting with <code>#</code> are comments. There are 4 instructions in this file:

<ul>
<li><code>FROM</code>: References the base Docker image we'll build upon. This is a powerful feature of Docker, allowing you to build incrementally more specific images. All we need to run the app is the Java 8 JRE, so we're building on top of <code>openjdk:8-jre</code>.</li>
<li><code>WORKDIR</code>: This changes the working directory inside the image filesystem. It's the folder where we'll place the jar of the application.</li>
<li><code>COPY</code>: As the name suggests, it copies the application's jar into the image. The left side references the host filesystem, so that's the Maven target folder containing the generated jar. The right side is in the image, relative to the previously specified working directory (<code>WORKDIR</code>).</li>
<li><code>CMD</code>: This is the command that the container will run. It's the java command line you might expect.</li>
</ul>

If we have this <code>Dockerfile</code> at the root of the project, we can build
a new image. First we need to prepare the jar with <code>mvn packge</code> and
then we build the image like this:

```sh
docker image build -t consumer .
```

This builds an image called <code>consumer</code> and uses the Dockerfile on the
current folder (that's the <code>.</code> argument). We can run the image:

```sh
docker run --name consumer consumer
```

This will run the <code>consumer</code> <em>image</em> (last argument) into a
new <em>container</em> named also <code>consumer</code> (that's the
optional <code>--name consumer</code> argument). If everything goes fine, the
user consumer will start, waiting for messages.

<h3>Single jar</h3>

In general, things are easier when the application consists of a single file (jar, war, whatever). It is possible to produce a jar in which all the dependencies are packaged together with the <code>maven-assembly-plugin</code>. We'll need this <code>plugin</code> declaration in the pom:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-assembly-plugin</artifactId>
    <version>3.0.0</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>single</goal>
            </goals>
        </execution>
    </executions>
    <configuration>
        <descriptorRefs>
            <descriptorRef>jar-with-dependencies</descriptorRef>
        </descriptorRefs>
    </configuration>
</plugin>
```

When we run <code>mvn package</code>, this will kick in automatically and create
an additional jar named
<code>kafka-playground-1.0-SNAPSHOT-jar-with-dependencies.jar</code>. The size
of the plain jar is 12K while this new jar weighs in at 4.5MB, so batteries are
included.

<h3>Enabling Debugging and structure for multiple Dockerfiles</h3>

To debug our app, we need to run it with a different command. The java command
needs one extra parameter:

```
-agentlib:jdwp=transport=dt_socket,address=50505,suspend=n,server=y
```

where 50505 is the port we'll use for debugging. It can be any port, it's up to
us. Since debugging is done over the network, that also means we need to expose
that port in Docker. In any case, we need a different Dockerfile.

According to <a
href="https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/"
target="_blank">Docker best practices</a>, it’s best to put each Dockerfile in
an empty directory. We still need our old Dockerfile for regular run (e.g.
production) and we need a new one for debugging only. This is where we need to
add some structure to the project.

We'll create a folder called <code>docker</code> and inside that two folders:
<code>debug</code> and <code>release</code> (that's my .NET background kicking
in). In the <code>release</code> folder, we'll place our current Dockerfile. In
the <code>debug</code> folder, we'll create this new Dockerfile:

```dockerfile
FROM openjdk:8-jre

# change directory to where the app will live
WORKDIR /usr/local/playground/

# install the jars
COPY target/*.jar ./

# remote debugging port for IntelliJ
EXPOSE 50505

CMD ["java", \
    "-agentlib:jdwp=transport=dt_socket,address=50505,suspend=n,server=y", \
    "-cp", \
    "kafka-playground-1.0-SNAPSHOT.jar:*", \
    "ngeor.UserConsumer"]
```

Notice the differences:
<ul>
<li>we use the <code>EXPOSE</code> instruction to tell Docker that the container will be listening to this port.</li>
<li>the <code>CMD</code> instruction contains the extra argument that enables debugging. Also it is broken down for readability</li>
</ul>

To build the debugging Docker image, we'll have to run this command:

```sh
docker image build -t consumer-debug ./docker/debug/
```

But, it does not work! That's because the COPY command fails. Host paths are
relative to the Dockerfile, so it's looking for <code>target/*.jar</code> inside
our new <code>docker/debug</code> folder. You can try
<code>../../target/*.jar</code> but that also does not work. By design, Docker
does not allow you to include things outside the folder hierarchy defined by the
folder where the Dockerfile lives. In other words, we'll have to bring the jar
into that folder.

I implemented that with the <code>mavent-antrun-plugin</code>. It allows you to
run Ant targets during Maven execution. In this example, we copy the generated
jar from the target folder into the new docker folders:

```xml
<properties>
    <single.jar.descriptor>jar-with-dependencies</single.jar.descriptor>
    <single.jar.file>target/${artifactId}-${version}-${single.jar.descriptor}.jar</single.jar.file>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-antrun-plugin</artifactId>
            <version>1.8</version>
            <executions>
                <execution>
                    <phase>package</phase>
                    <goals>
                        <goal>run</goal>
                    </goals>
                </execution>
            </executions>
            <configuration>
                <target>
                    <echo message="Copying package to docker/debug folder" />
                    <copy
                        file="${single.jar.file}"
                        todir="docker/debug/target" />
                    <echo message="Copying package to docker/release folder" />
                    <copy
                        file="${single.jar.file}"
                        todir="docker/release/target" />
                </target>
            </configuration>
        </plugin>
    </plugins>
</build>
```

Notice that I have preserved the target folder inside
<code>docker/debug</code> and <code>docker/release</code>, because it is already
part of my <code>.gitignore</code>. This is how the folder structure looks like:

<img src="{{ site.baseurl }}/assets/2017/docker-folders.png" />

It's a good idea to also cleanup after ourselves. It would be great to delete
the new copies of the jar file when we run <code>mvn clean</code>. For that
reason, we'll need this configuration:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-clean-plugin</artifactId>
    <version>3.0.0</version>
    <configuration>
        <filesets>
            <!-- delete jar files copied into docker folders -->
            <fileset>
                <directory>docker</directory>
                <includes>
                    <include>**/*.jar</include>
                </includes>
            </fileset>
        </filesets>
    </configuration>
</plugin>
```

And we're all set.

<h3>IntelliJ plugin</h3>

The IntelliJ plugin is called Docker Integration and it's provided by JetBrains.
It offers various features:

<ul>
<li>syntax highlighting for Dockerfiles</li>
<li>managing the Docker instance, e.g. start/stop/delete containers, delete images</li>
<li>enables debugging into Docker, implemented as an IntelliJ run configuration</li>
</ul>

First of all, it needs to know where our Docker is:

<img src="{{ site.baseurl }}/assets/2017/docker-intellij.png" />

It is quite smart, you probably won't have to do much typing. You'll find it
sitting at the bottom toolbar:

<img src="{{ site.baseurl }}/assets/2017/docker-toolbar.png" />

The green play button connects you to Docker:

<img src="{{ site.baseurl }}/assets/2017/docker-connected.png" />

Notice that it lists existing containers and images. The containers are all
stopped. I can right click the "hp-kafka" container and run it:

<img src="{{ site.baseurl }}/assets/2017/docker-container-running.png" />

Notice that the icon changes into a filled light blue box.

To be able to debug our app, we need a new debug configuration:

<img src="{{ site.baseurl }}/assets/2017/debug-configuration-fix.png" />

Let's take this step by step:

<ul>
<li>The configuration is shared, so that we can put it in git and share it with developers (more on that later)</li>
<li>The server is the local Docker we configured earlier</li>
<li>The deployment drop down allows to select one of the Dockerfiles in the project (detected automatically) or an existing image. We'll go for the Dockerfile approach.</li>
<li>The container name is just a name to identify the container by</li>
<li>Notice the debug port, 50505 matching what our Dockerfile mentions. Notice also how helpful the plugin is, telling you the argument you will need in order to enable debugging (yes, that's where I got it from)</li>
<li>Very important: before launch, run mvn package. This is why we did all the proper Maven setup and the folder structure according to best practices, so that the IntelliJ configuration is as minimum as possible.</li>
</ul>

Notice the warning at the end about "Debug port forwarding not found". Our
Dockerfile is correct. However, the <code>EXPOSE</code> directive just informs
docker that the container listens to the 50505 port. When creating the
container, you still have to tell it to forward that port so that it's
accessible outside the container. If we were starting the container ourselves,
that would be the <code>-p 50505:50505</code> flag. Here, it's IntelliJ that
will be starting the container, so it raises the warning. The fix button does
that. It offers to create a json file with the needed container settings. Save
it side-by-side with the debug Dockerfile, so that it's clear it is only needed
for debugging:

<img src="{{ site.baseurl }}/assets/2017/docker-container-settings.png" />

And with this the warning disappears:

<img src="{{ site.baseurl }}/assets/2017/debug-configuration.png" />

The container settings looks like this:

```json
{
  "HostConfig": {
    "PortBindings": {
      "50505/tcp": [
        {
          "HostIp": "0.0.0.0",
          "HostPort": "50505"
        }
      ]
    }
  }
}
```

<h3>Debugging</h3>

We can finally debug! We start the debug configuration with the debug icon.
IntelliJ switches to the Debug panel:

<img src="{{ site.baseurl }}/assets/2017/debug-connected.png" />

If you don't see this message immediately, you need to go back and see if
everything is configured correctly.

In the Docker panel, we see the container running:

<img src="{{ site.baseurl }}/assets/2017/docker-deploy-log.png" />

and we can also see the messages our app is printing:

<img src="{{ site.baseurl }}/assets/2017/docker-app-log.png" />

Let's put a breakpoint on the line where a new message is received from Kafka:

<img src="{{ site.baseurl }}/assets/2017/breakpoint.png" />

To hit that breakpoint, we'll need to actually send a message. Let's start the
producer. This is not a Docker container, just a regular Java app:

<img src="{{ site.baseurl }}/assets/2017/start-producer.png" />

IntelliJ allows you to run all sorts of things at the same time, so we can
manage everything from the same IDE window. The producer is interactive, so we
type the user information at the console:

<img src="{{ site.baseurl }}/assets/2017/producer-input.png" />

As soon as we enter all information, the message is sent and the breakpoint is hit:

<img src="{{ site.baseurl }}/assets/2017/breakpoint-hit.png" />

The experience is the same as with local debugging, you can see the variables,
the call stack, etc.

<h3>Sharing the debug configuration</h3>

One minor thing I found is that it's useful to share the debug configuration
within the team. Normally, I exclude all IntelliJ files from git. I think this
one is useful, so I've adjusted the gitignore like this:

```
#
# IntelliJ
#
*.iml
.idea/*
!.idea/runConfigurations/
```

I see we're doing this wrong currently at work, where every developer creates
run/debug configurations independently.

<h3>Lessons</h3>

<ul>
<li>read about the best practices regarding Dockerfiles</li>
<li>before jumping into the IDE, understand what is happening under the hood</li>
<li>use maven as much as possible. Everything that is possible through the IDE should be first be possible via the command line</li>
<li>single jar with all dependencies is easier to manage</li>
<li>share the debug configurations with the team</li>
<li>debugging inside a container is cool!</li>
</ul>
