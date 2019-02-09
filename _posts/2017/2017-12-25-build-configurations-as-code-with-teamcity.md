---
layout: post
title: Build configurations as code with TeamCity
date: 2017-12-25 09:41:36.000000000 +01:00
published: true
categories:
- continuous-delivery
tags:
- blog-helm-sample
- TeamCity
---

In this post, I'll show how to setup TeamCity so that your project's build configurations are stored in your git repository. This allows you to change your build configuration in the same way you change your code, via a pull request. It allows to make changes to the pipeline without affecting other branches. And all that is supported in a way that you don't have to give up the user friendly way of defining your build via the UI.

<!--more-->

I'm going to use the <a href="https://github.com/ngeor/blog-helm">blog-helm</a> project that I had configured in the <a href="{{ site.baseurl }}/cd-with-helm.html">CD with Helm series</a>. In TeamCity, the project had two build configurations:

<figure><img src="{{ site.baseurl }}/assets/2017/12/25/08_20_48-projects-e28094-teamcity.png" /><figcaption>Project with two build configurations</figcaption></figure>

First, edit the project and find the versioned settings section:

<figure><img src="{{ site.baseurl }}/assets/2017/12/25/08_24_14-blog-helm-project-_-versioned-settings-e28094-teamcity.png" /><figcaption>Versioned Settings - Before the changes</figcaption></figure>

In this form, we enable synchronization, specify the git repository (blog-helm) to use, select 'use settings from VCS' and finally use the Kotlin format:

<figure><img src="{{ site.baseurl }}/assets/2017/12/25/08_26_46-blog-helm-project-_-versioned-settings-e28094-teamcity.png" /><figcaption>Versioned Settings - After the changes</figcaption></figure>

Once you do this, TeamCity will commit to the master branch a bunch of files that describe everything under the project: in my case that's the two build configurations (Commit Stage and Deploy Stage) but also the VCS root definition of the project. Make sure TeamCtiy has write access to your git repository, otherwise it won't be able to push these changes.

After this is done, we can get latest and see that we have a new folder named <code>.teamcity</code> in our repository:

<figure><img src="{{ site.baseurl }}/assets/2017/12/25/08_41_52-blog-helm-visual-studio-code.png" /><figcaption>Versioned settings</figcaption></figure>

It should be straightforward enough: everything is under <code>.teamcity</code>. The first subfolder is the name of the project, <code>BlogHelm</code>. Build configurations are under the <code>buildTypes</code> subfolder and the VCS root is under the <code>vcsRoots</code> subfolder.

The settings are written in Kotlin. I don't know Kotlin but that's not a problem because the DSL is simple enough to make sense. In my opinion, it's more readable than editing XML files (which is an alternative option). For example, here's the DSL for running an inline shell script:

```
        script {
            name = "Radically changing build"
            scriptContent = """
                echo "Hello, world!"
            """.trimIndent()
        }
```

I think it's much easier to start with an existing project and export it, so that you'll get a taste of what folders and files you get.

Now that we have this in our git repository, these settings are leading. Settings still exist in TeamCity, but the ones in our git repository take precedence and override the ones in TeamCity. This opens up a window of opportunity: we can modify the build pipeline in a feature branch. This is extremely useful when you have a breaking change in a feature branch which involves a corresponding change to the build pipeline. Normally, that would be a chicken-egg problem where your branch would be red until you modify the pipeline, but doing that would cause everybody else's branch to turn red. Having the pipeline versioned in code means that you can do these changes in an isolated manner.

As an example, I'll create a feature branch that has an extra build step which prints out some diagnostic information, e.g. the Docker version we're using. I'll do that with an inline script which just runs "docker version".

First, I create a new feature branch out of master, named <code>add-diagnostics-step</code>. I'll modify the <code>BlogHelm_CommitStage.kt</code> file by injecting a schell script step at the start, right above the previous first step:

```
steps {
    script {
        name = "Basic diagnostics"
        scriptContent = """
            docker version
        """.trimIndent()
    }
    exec {
        name = "Ensure feature branch is ahead of master"
        path = "ci-scripts/merge.sh"
    }
```

When I push these changes, the build will start with the settings defined in that branch. We can see that in the log of the build:

<figure><img src="{{ site.baseurl }}/assets/2017/12/25/09_04_48-blog-helm-__-commit-stage-_-1-3-2-add-diagnostics-step-1-25-dec-17-08_02-_-bu.png" /><figcaption>Feature branch with extra build steps</figcaption></figure>

Our new build step was executed and it worked fine. Since this is just a feature branch, TeamCity will still report 7 build steps via the UI:

<figure><img src="{{ site.baseurl }}/assets/2017/12/25/09_06_47-commit-stage-configuration-e28094-teamcity.png" /><figcaption>Before merging the feature branch</figcaption></figure>

If we merge the feature branch into master, TeamCity will show the new step in the UI:

<figure><img src="{{ site.baseurl }}/assets/2017/12/25/09_13_14-commit-stage-configuration-e28094-teamcity.png" /><figcaption>After merging the feature branch</figcaption></figure>

What happens if you still want to use the UI? TeamCity allows you to do so. Once you modify something in your build, TeamCity will commit the changes to the master branch. However, it won't modify the existing files. It will create instead a patch file, containing only the change you did, with instructions on how to merge the patch back to where it belongs and then delete it. This is an interesting design choice. They could've just opted for overwriting the files directly, but perhaps that could've lead to some conflicts.

As an example, I'll modify the newly created diagnostics step to also print the Linux version the agent is running (with <code>lsb_release -cdir</code>):

<figure><img src="{{ site.baseurl }}/assets/2017/12/25/09_18_42-todoist_-to-do-list-and-task-manager.png" /><figcaption>Modifying the build with the UI</figcaption></figure>

This will create a new commit in master branch, with a new folder named <code>patches</code>, containing the change:

<figure><img src="{{ site.baseurl }}/assets/2017/12/25/09_22_33-3f8adc5d-5b14-4a13-9ecd-70b624f828de-kts-blog-helm-visual-studio-code.png" /><figcaption>Patch file</figcaption></figure>

The patch file mentions the expected steps and finally contains the actual change:

```
    steps {
        update<ScriptBuildStep>(0) {
            scriptContent = """
                lsb_release -cdir
                docker version
            """.trimIndent()
        }
    }
```

These UI patches are meant to be temporary and they should be applied to the code and deleted.

Having the build configuration is git is a great feature. Once something is in git, it obeys to the same rules as code does. It is open to anyone to read and experiment with. There are no special people in the team that have special access to configure the build, anyone can do it. Build configuration changes are subject to code review. And feature branches allow for introducing breaking changes to the build pipeline without impacting others.

Another interesting thing to observe is that having the build configuration in git makes it easier to use (and abuse) inline shell scripts. It's often handy to add a little bit of ad-hoc inline bash in a build step, but if it's not under git you risk losing it, it's not transparent, etc. Now, these little steps become part of git just like everything else. It's probably a good idea to still use separate files for shell scripts (especially larger ones), as it will be clearer in the code review what you're changing, you'll be able to test them locally, you'll have syntax highlighting, and so on.
