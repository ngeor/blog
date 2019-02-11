---
layout: post
title: How to deploy a smashing dashboard to AWS Elastic Beanstalk with Docker
date: 2017-05-09 19:53:13.000000000 +02:00
published: true
categories:
- programming
tags:
- AWS
- dashboard
- docker
- Elastic Beanstalk
- smashing
---

So, <a href="{{ site.baseurl }}/2017/05/08/how-to-build-a-smashing-dashboard.html">in the previous post</a> we created a fancy dashboard using the smashing framework. Let's see how we can deploy our dashboard to AWS Elastic Beanstalk using Docker.

<!--more-->

AWS Elastic Beanstalk <a href="https://aws.amazon.com/elasticbeanstalk/faqs/" target="_blank" rel="noopener noreferrer">supports</a> various platforms and programming languages, such as Java, nodeJS, .NET, Python, and also Ruby, the language our dashboard is using. However, it doesn't seem to work out of the box for the smashing dashboard. I didn't dive into it, but I can imagine that the reason is that we are using a custom command to start the dashboard ( <code>smashing start</code> ) and perhaps that's too exotic for AWS. But, no worries. AWS Elastic Beanstalk supports Docker as well. As long as we can package the dashboard application inside a Docker container, everything should be good.

Docker is so popular, that it's very likely someone (or more than one) will already have created a Docker image for your needs. This is also the case for the smashing dashboard. I found <a href="https://hub.docker.com/r/rgcamus/alpine_smashing/" target="_blank" rel="noopener noreferrer">this image</a> which works quite nice. The documentation is enough, but I also like to peek into the <a href="https://github.com/rgcamus/dockerfile-alpine_smashing/blob/master/Dockerfile" target="_blank" rel="noopener noreferrer">Dockerfile</a> to have an understanding of what is happening under the hood. This image is quite extensible, but let's see if it covers what we need.

We have of course written custom code. Dashboards, jobs and widgets, each in their own folder. Well, it offers mount points (volumes) for all source code folders. This means we can mount the source code folders, inside the Docker container, without baking them into a custom image. We are also using additional gems (rest-client and json). This Docker image happens to support passing additional gems on the fly using an environment variable. And that's all actually. All our customizations are covered.

To try it locally, we need to run something like this:

```

docker run -d \
-p 80:3030 \
-v ./dashboards:/dashboards \
-v ./jobs:/jobs \
-v ./widgets:/widgets \
-e GEMS="rest-client json" \
rgcamus/alpine_smashing

```

Let's review the arguments:
<ul>
<li>-d: run it in detached mode (background), so that the console is not blocking</li>
<li>-p: map port 80 of the host into port 3030 of the Docker image</li>
<li>-v ./dashboards:/dashboards : map the local ./dashboards folder (based on the current directory) into the /dashboards volume of the Docker image. The rest of the -v arguments are for the jobs and widgets folders.</li>
<li>-e: define the environment variable GEMS as "rest-client json" (the Docker image uses it to install the gems)</li>
</ul>

In AWS ElasticBeanstalk, you typically upload a zip file with your application and AWS knows how to deploy it. In this case however, we need to pass multiple command line options, somehow. To solve this problem, AWS defines its own way of configuring a Docker container: by placing inside the zip file a JSON file named <code>Dockerrun.aws.json</code>. This file tells AWS how it should create the Docker container. It's essentially the same as the command line arguments of the docker command, but in a JSON file format defined by AWS.

There are two flavors of this file. Version 1 is for single container applications, version 2 is for multi-container. Just as an example, this is how the JSON file looks like in the multi-container flavor:

```javascript
{
	"AWSEBDockerrunVersion": 2,
	"volumes": [
		{
			"name": "dashboards",
			"host": {
				"sourcePath": "/var/app/current/dashboards"
			}
		},
		{
			"name": "jobs",
			"host": {
				"sourcePath": "/var/app/current/jobs"
			}
		},
		{
			"name": "widgets",
			"host": {
				"sourcePath": "/var/app/current/widgets"
			}
		}
	],
	"containerDefinitions": [
		{
			"name": "dashboard",
			"image": "rgcamus/alpine_smashing",
			"memory": 256,
			"environment": [
				{
					"name": "GEMS",
					"value": "rest-client json"
				}
			],
			"portMappings": [
				{
					"hostPort": 80,
					"containerPort": 3030
				}
			],
			"mountPoints": [
				{
					"sourceVolume": "dashboards",
					"containerPath": "/dashboards"
				},
				{
					"sourceVolume": "jobs",
					"containerPath": "/jobs"
				},
				{
					"sourceVolume": "widgets",
					"containerPath": "/widgets"
				}
			]
		}
	]
}
```

It's definitely more verbose compared to the command line arguments, but it is equivalent. The <code>"/var/app/current"</code> folder is just where AWS unzips the zip folder in the host.

Notice that we didn't have to provide a Dockerfile at all. That's because we were lucky and someone had created a Docker image that covers all of our requirements. To deploy the app to AWS Elastic Beanstalk, we just need to create a zip file that creates the Dockerrun.aws.json file, together with the code folders of our app (dashboards, jobs, widgets).

<img src="{{ site.baseurl }}/assets/2017/05/09/21_39_13-dashboard2-env-dashboard-e2808e-microsoft-edge.png" />

This simple exercise is a nice example of how Docker solves infrastructure obstacles. Instead of figuring out what it takes for AWS to support our exotic stack, we provide a Docker container that just works.
