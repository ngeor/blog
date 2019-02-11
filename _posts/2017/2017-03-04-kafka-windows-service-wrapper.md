---
layout: post
title: Kafka Windows Service Wrapper
date: 2017-03-04 06:36:16.000000000 +01:00
published: true
categories:
- pet-projects
tags:
- Kafka
- Windows Service
- ZooKeeper
---

TL;DR: I created a wrapper for Apache Kafka so that it can be installed as a Windows Service. In this post I also describe a bit what Kafka is.

<!--more-->

We have started using Apache Kafka at work and it's brand new to me. What is Kafka? According to Wikipedia: "it is an open-source stream processing platform which aims to provide a unified, high-throughput, low-latency platform for handling real-time data feeds". If I would describe it in my own words, I'd say it's a publish-subscribe messaging broker, built with scalability in mind. You can publish a message to a Kafka topic and Kafka will deliver the message to any consumer that has subscribed to that topic. You can think of a topic like a database table and a message like a record in that table. You can assign more consumers to process the same topic, creating a consumer group, with the result of scaling up with processing power.

Embracing Kafka can create a unified way of communication across systems. In our current landscape at work, communication is far from unified. All sorts of systems communicate with others (including external vendor systems) in all sorts of protocols. This is for both sending and receiving data. When receiving, it is not uncommon to have a polling loop, trying to read data from a remote shared location (such as an FTP folder). From an architecture point of view, Kafka can clean this up. All internal systems can start talking to each other with messages. To be more precise, they don't talk to each other. They simply subscribe to what they're interested in and they broadcast what others might be interested in. The coupling is gone. And of course we can't change the whole world, external vendors will still have their legacy interfaces. Kafka however acknowledges this by providing a concept called Connector, which converts an old school data source into a Kafka messaging stream.

You may be wondering, wait, did you just create a single point of failure? Well, that is indeed true. With Kafka sitting in the middle of the universe, if it goes down, everything goes down with it. Kafka needs to be treated as an always available system and be setup as such. For this reason, Kafka needs to be accompanied by Apache ZooKeeper. ZooKeeper takes care of a cluster of Kafka nodes and makes sure the system is always on. If a Kafka node fails, the next one in the cluster is asked to do the job.

So, like I said, we started using Kafka. How do you use it locally, on your developer's machine? Kafka has a great <a href="https://kafka.apache.org/quickstart" target="_blank">quickstart</a> page. You just download and unzip a folder and you have a working ZooKeeper and Kafka. Both these services are controlled by batch files. There's a batch file that starts ZooKeeper and a different one that terminates the service. Same for Kafka.

On a Windows machine, that can be a bit tedious to do all the time. It would be great if we could install these as regular Windows services and have them start automatically. I googled a bit first to see if there's anything already built. I found a <a href="https://github.com/lukemerrett/Kafka-Windows-Service" target="_blank">project in GitHub</a> and a <a href="http://stackoverflow.com/questions/36309844/install-kafka-as-windows-service" target="_blank">SO question</a> asking the same thing.

I'll start with the SO question. The answer there involved using some free tool to create the service wrappers. When I tried to go to the tool's page, I got a SSL warning in my browser. I get a bit off topic here, but allow me to say this: if your site has a broken SSL certificate, your site does not exist to me. Period.

So I went to the next option, I evaluated a bit the project I found in GitHub. This was very very close to what I wanted but it had some problems:
<ul>
<li>it contained hard-coded paths to the Kafka installation folder. So if I had unzipped Kafka in a different place, it wouldn't work.</li>
<li>it used some library called TopShelf to define the Windows Service. I don't know this library, so I don't know if it's a good idea to add a third party dependency for this.</li>
<li>it did a bit more than what I wanted: it can also download Kafka automatically if it's missing. I think that's a bit too much.</li>
</ul>

That's why I created my own wrapper service. You can find it <a href="https://github.com/ngeor/kafka-windows-service-wrapper" target="_blank">in GitHub</a>. The original prototype was done in almost an hour. But when I rebooted my computer, things didn't work as expected, so I built in a bit more features.

The most important one: it patiently waits for ZooKeeper to start listening on its port (port 2181 by default) before allowing Kafka to start. Let's explain this bit by bit. Kafka needs ZooKeeper. If you try to start the Kafka batch file and ZooKeeper is not up and running, Kafka dies. The trick here lies in the definition of "up and running". In the original prototype, the wrapper service launches the batch file and claims everything is ready. This gives the signal to Windows to also start the Kafka service. However, it takes a second or two for ZooKeeper to actually become ready and start listening for connections. When these things are happening by the OS, and not by a human double clicking on batch files, you can end in Kafka starting before ZooKeeper being ready to serve. I solved this by adding an extra wait in the ZooKeeper windows service wrapper. After launching the batch file, the windows service waits until the port is reachable.

The second problem is a bit shadier and I didn't really solved it, I just patched it enough. This has to do with restarting services. It's easy in Windows to right click a service and restart it. The problem here is that Kafka would sometimes die. From what I figured out from its error logs, it said something like the restart might have happened to fast for ZooKeeper to mark this as an unregister operation, or something like that. I patched this one by adding an extra delay of 5 seconds after launching a batch file.

Another cool thing I added: if the underlying process dies unexpectedly, I add an error to Windows Event Log and the windows service also transitions into a stopped state.

Well, I hope someone else will also use this and find it useful. Future improvement ideas:
<ul>
<li>to be able to have the log messages also available inside the Windows Event Log</li>
<li>get rid of the batch files and run whatever they're running directly</li>
<li>create an installation package for the service wrapper, potentially bundled with Kafka, so you have a Windows developer-friendly installer</li>
<li>Binaries are available through AppVeyor but you still need installutil to install them. Next point: make the service able to install itself as described <a href="http://stackoverflow.com/questions/1195478/how-to-make-a-net-windows-service-start-right-after-the-installation/1195621#1195621" target="_blank">here</a>.</li>
</ul>
