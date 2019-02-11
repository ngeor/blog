---
layout: post
title: 'Kafka with Docker: A Docker introduction'
date: 2017-03-25 08:47:07.000000000 +01:00
published: true
categories:
- programming
tags:
- docker
- Kafka
- Kafka Tool
featured: true
---

Using Kafka on your local development machine adds another level of complexity. You need to manage two extra services, Apache ZooKeeper and Apache Kafka. In a previous post, I mentioned the possibility of creating <a href="{{ site.baseurl }}/2017/03/04/kafka-windows-service-wrapper.html">a Windows service wrapper for Kafka</a>, so that managing is a bit easier. In this post, we'll have a look at Docker and how we can use it to solve the same problem in a different way. I am new to Docker, so this is a very basic post, more like an introduction to Docker.<!--more-->

Docker is a technology similar to virtual machines, but more efficient. You can have a Docker container that runs a service (e.g. a database, a web server, Kafka, whatever). The service is completely isolated from the host, just like with virtual machines. However, you don't pay the overhead of a full blown guest OS running the service. Docker removes the need for the guest OS, while keeping the containers isolated. The other strength of Docker is the community. There are many images that already have what you want (e.g. a plain Ubuntu image, or a Tomcat image, etc). It's also easy to create new images.

A small note about Windows 10 Home, which is what my laptop is running. Microsoft's Hyper-V virtualization technology is not available on Windows 10 Home. This is what Docker relies on on Windows. The workaround is to install VirtualBox and <strong>Docker Toolbox</strong>. Since my laptop runs Windows 10 Home, this is what I'll be using in this post. It doesn't change anything regarding the commands we have to run.

We start Docker with the <strong>Docker Quickstart Terminal</strong>. Eventually you are greeted with a bash shell:

<img src="{{ site.baseurl }}/assets/2017/docker-shell.png" />

Two interesting things in the message below the ASCII whale:
<ul>
<li>it has created and using behind the scenes a VirtualBox machine named default</li>
<li>the IP for that machine is 192.168.99.100 - this is important because that's where our services will be publishing themselves. So if you would publish a small website with Docker, it would be available at http://192.168.99.100/ and not at http://localhost/</li>
</ul>

Actually, we're ready to start Kafka. Turns out there are already <a href="https://store.docker.com/search?q=kafka&source=community&type=image" target="_blank">Docker images for Kafka</a> available in <strong>Docker Store</strong>. I am going to use the <a href="https://store.docker.com/community/images/spotify/kafka" target="_blank">spotify image</a> because it seems to be rather basic (also because I recognize the spotify name...). Following the instructions, this is how we start Kafka:

<img src="{{ site.baseurl }}/assets/2017/docker-kafka-command-line.png" />

The command is:

```

docker run -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=192.168.99.100 --env ADVERTISED_PORT=9092 spotify/kafka

```

or broken down for readability:

```

docker run \
  -p 2181:2181 \
  -p 9092:9092 \
  --env ADVERTISED_HOST=192.168.99.100 \
  --env ADVERTISED_PORT=9092 \
  spotify/kafka

```

Points of interest:
<ul>
<li>the -p flag is used to publish a network port. Inside the container, ZooKeeper listens at 2181 and Kafka at 9092. If we don't publish them with -p, they are not available outside the container, so we can't really use them.</li>
<li>the --env flag sets up environment variables. These are needed as per the documentation of the spotify/kafka image</li>
<li>the last part specifies the image we want to run: spotify/kafka</li>
</ul>

That's it actually. Docker will realize it doesn't have the spotify/kafka image locally, so it will first download it:

<img src="{{ site.baseurl }}/assets/2017/docker-download.png" />

and once that's done, it will start Kafka:

<img src="{{ site.baseurl }}/assets/2017/docker-kafka.png" />

That's all there is to it. You can verify that everything is working as expected with the test kafka-console-producer and kafka-console-consumer tools. Or you can use a UI tool like <a href="http://www.kafkatool.com/" target="_blank">Kafka Tool</a> to attempt to connect to Kafka.

<img src="{{ site.baseurl }}/assets/2017/kafka-tool.png" />

You can also use this tool to create a topic and send/receive messages:

<img src="{{ site.baseurl }}/assets/2017/kafka-tool-message.png" />

This proves that our Kafka installation works fine.

To shutdown the Docker container, we need its ID. We can find that with the command <code>docker container ls</code>. Then we run <code>docker container stop containerID</code> and Kafka shuts down. Docker is quite smart, you don't have to type the full ID, just a few letters of it. Starting it again is done with <code>docker container start containerID</code>. Everything will be as we left it.

Since this is Windows 10 Home and we're using Docker Toolbox, we still have a virtual machine running somewhere behind the scenes. If we also want to terminate that, we run the command <code>docker-machine stop</code>. The virtual machine will start again automatically when we start Docker Quickstart Terminal.

Docker offers multiple advantages in the developer's workflow:
<ul>
<li>the host OS is kept clean and doesn't accumulate all sorts of services to bog it down.</li>
<li>it can be used the same way regardless of whether the developer is using Windows, Mac or Linux</li>
<li>there are many ready made images to pick from to get you up running fast</li>
<li>it is possible to combine multiple containers at once (e.g. database server, application server, etc)</li>
</ul>

And it is also possible to use Docker directly on production, but that's a whole other discussion.
