---
layout: post
title: Docker hacking session
date: 2017-06-04 06:17:41.000000000 +02:00
published: true
categories:
- Tech Notes
tags:
- docker
- hackathon
- spring
---

Last week I organized a hacking session for my team at work. We ordered pizzas and we stayed a couple of hours extra to have a look at Docker. For some people this was completely new, for some others not as much. The feedback however was positive overall.

Here's what we covered initially:
<ul>
<li>Docker introduction and some concepts. What is Docker? What is a Docker image? What is a Docker container?</li>
<li>Hands on (after all this is a hacking session): Install Docker on our laptops and run the <a href="https://docs.docker.com/get-started/#setup" target="_blank" rel="noopener noreferrer">hello world</a> (some folks had Windows 7 laptops so they installed Docker Toolbox instead).</li>
<li>Introduction to <a href="https://docs.docker.com/get-started/part2/#define-a-container-with-a-dockerfile" target="_blank" rel="noopener noreferrer">Dockerfile</a>. We went over the instructions. We discussed ports, volumes, environment variables and base images.</li>
<li>Introduction to Docker Store (formerly Docker Hub). Discussed certified images, popular images, etc.</li>
</ul>

From there, we created a simple Spring Boot application and dockerized it (following <a href="https://spring.io/guides/gs/spring-boot-docker/" target="_blank" rel="noopener noreferrer">this guide from Spring</a>):
<ul>
<li>First, we created a hello world Spring Boot web application. To some people this was also new, so we stayed on this point for a bit longer.</li>
<li>We created a Docker image for the app using Docker's CLI.</li>
<li>We created a Docker image for the app using the Spotify Maven plugin.</li>
<li>Finally, we published the custom Docker image to AWS ECR.</li>
<li>Just when we ran out of time, we briefly took a glance at docker-compose as well.</li>
</ul>

In my opinion, the success of a hacking session depends on the participation of the joiners (and that's why our session turned out quite nice). This is not like a meetup where you go and hear someone speaking. In a hacking session, you have to join with a hands on experimenting mentality. You type, you search, you figure it out, you learn, you have fun!

(The photo is from the 1995 movie Hackers, but you already knew that)
