---
layout: post
title: Automatically upgrade parent pom
date: 2019-02-16
published: true
tags:
  - python
  - bitbucket
  - maven
  - microservices
  - dependencies
  - parent pom
---

TL;DR: I wrote a script that discovers git repositories with an outdated parent
pom and then it creates a pull request on each repository to set the parent pom
version to latest and greatest.

A bit of background information: at work, we have at the moment something around
30 microservices. They all share the same technology stack, which makes it easy
for developers to use existing services as examples for building new features
and eliminates the overhead of context switching (I can't stretch enough how
important that is). All services are based on Java and Spring Boot (Spring
everything really). We use Maven to build the projects and manage dependencies.

Speaking of dependencies, we have our own parent pom project to specify the
versions of the plugins and dependencies. **All projects inherit from that
parent pom**, which in turn inherits from Spring Boot's parent pom.

When we want to upgrade a dependency (e.g. use the latest version of Mockito),
we do that first in the parent pom. We change the desired version of Mockito
there and bump the version of the parent pom. The upgrade of the services
themselves to the latest parent pom happens eventually, typically when someone
is working on a service and notices that there's an upgrade available. If we're
not busy with a service, it will stay with its current parent pom version (if it
ain't broken, don't fix it). There's no strict process around it.

That's all fine and it works so far. It might be annoying (and to me it is a
bit) knowing that some services are not on the latest and greatest, but it's not
critical.

Wait. What if it _were_ critical? What if the upgrade is not a nice to have but
a security fix for a vulnerability? Then you'd probably want to **upgrade
everything as soon as possible**.

Upgrading the version of the parent pom is something that can be automated. And
if it can be automated, then it should (hashtag automate all the things).

Here's what needs to happen:

- get the latest version of the parent pom (literally open the `pom.xml` and
  read the version)
- get a list of projects that use the parent pom
- for each project, set the version of the parent pom to the latest, commit the
  `pom.xml` and create a PR
- make sure you don't do this if the version is already the latest
- make sure you don't do this if a PR is already open about this

The [python
script]({{ site.baseurl }}{% post_url 2019/2019-02-11-goodbye-bash %}) that does
all of the above weighs in at exactly 200 lines, and while it could probably be
improved a bit, it works on my cloud.

Some implementation trivia:

- Always use a dedicated user for automated processes, don't use your personal
  credentials.
- I had to use lxml instead of the built-in xml library, because this way I
  could preserve comments and CDATA sections inside the `pom.xml`.
- To figure out if a PR is already open, I just check if a branch with the magic
  name `upgrade-parent-pom` already exists.
- Getting the list of repositories and creating the PRs is done with Bitbucket
  Cloud REST API.
- The script runs as a scheduled job once per day. Since we use Kubernetes, I
  deployed it as a CronJob there, which is something I did for the first time
  and it worked quite nice. Getting the credentials in there requires a bit of a
  dance with Helm. It's all automated of course, part of the deployment
  pipeline.

This is what the main method of the script looks like:

```python
def main():
    parent_pom_version = get_parent_pom_version()
    print(f'Parent pom version: {parent_pom_version}')
    slugs = get_projects_to_upgrade(parent_pom_version)
    for slug in slugs:
        update_parent_pom_version(slug, parent_pom_version)
```

And this is the list of PRs that are now open for review (hurray):

![pull requests]({{ "assets/2019/02/pull-requests.png" | relative_url }})

A possible alternative could be for the script to push directly to master
instead of creating pull requests. That has some problems:

- it risks having a red master, as there is a possibility that the dependency
  upgrade might break a service. This hasn't happened so far but it is of course
  possible. Having a red master is not nice, and it's not like I can ask a bot
  to be please more careful next time.
- it risks having a deployment to production at an inconvenient moment. A green
  master gets automatically deployed to production and for whatever crazy reason
  you might have asked everyone to stop merging for a moment. Well, according to
  Murphy's law that's when the bot would merge (damn these bots were supposed to
  be our friends!)
- it would bypass the code review process, which is to say that the script is
  flawless. As it's written by a human (me), I'm pretty sure it will probably
  break one day when someone tries to put an emoji in a filename during daylight
  savings time change (as an example).

(oh and multiply the above by the number of microservices)

The nice thing with this type of automation is that it feels like having an
**extra team member** who watches over the codebase and takes care of it. You
don't need to remember to do it, you don't need to worry that you might forget
it.

And this is a first step for further workflows like this. Until then, here's a
fitting song:

<iframe width="560" height="315" src="https://www.youtube.com/embed/B1BdQcJ2ZYY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
