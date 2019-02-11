---
layout: post
title: Publishing my first Maven package with Travis
date: 2017-03-29 18:24:45.000000000 +02:00
published: true
categories:
- programming
tags:
- continuous integration
- maven
- Nexus
- travis
---

A little bit more than a month ago, I created an <a href="{{ site.baseurl }}/2017/02/25/a-quickstart-maven-archetype-for-java-8.html">improved Maven archetype project</a>. Similar to the default quickstart archetype, but for Java 8 and with recent jUnit dependency. In order for someone to use it, they'd have to clone the repo, as I had not published it in Maven. After a bit of studying, I figured out what is needed to make the package public. More importantly, I implemented the process in Travis, so that a new version gets published automatically.

<!--more-->

<strong>Where</strong> does one publish maven packages? That's the <a href="http://central.sonatype.org/" target="_blank">central repository</a>. That's the default repository where Maven will look up packages, if they haven't been downloaded locally already. There's also a <a href="http://search.maven.org/" target="_blank">search engine</a> for the central repository. It is also possible to browse directly into the repository structure, e.g. <a href="http://repo1.maven.org/maven2/org/apache/maven/plugins/" target="_blank">here you can see a folder per artifact</a> of the <code>org.apache.maven.plugins</code> group. This is where we need to publish.

<strong>How</strong> do we publish? There's <a href="http://central.sonatype.org/pages/producers.html" target="_blank">documentation</a> available, as well as some videos. It's not as easy as publishing a .NET package to NuGet or a nodeJS package to npm. In general, the experience feels rather old (just like the user interface of the underlying Nexus system) and a bit manual.

First, you need to create an account to the JIRA of Sonatype's Open Source Software Repository Hosting (OSSRH). Note that the same credentials will be used later to publish your package. In the JIRA ticket, you specify your group ID, artifact ID and some additional information. Based on some video from Sonatype, I got the suggestion of picking <code>com.github.ngeor</code> for my groupID. I think it's fair, since I don't really have my own domain and it's an open source project hosted on GitHub. Soon after the ticket is created, they confirm that you can start using those credentials to publish to their Nexus. Nexus is a repository manager. This product supports more types of repositories, e.g. npm and NuGet.

Publishing to a repository is something that maven understands already. We don't have to do too much work there. However, there are extra <strong>requirements for the quality of the package</strong> and that is what makes setting up this task a bit tricky. Another reason why we must automate this process with Travis. The requirements are:
<ul>
<li>the POM needs to have various informative elements, such as license, developers, etc.</li>
<li>the package needs to include documentation (javadoc) and source code</li>
<li>the package needs to be signed with GPG.</li>
</ul>

Let's see the requirements in more details.

Regarding the POM, it needs some elements you may be missing:
<ul>
<li>name (the name of the project)</li>
<li>description (a more detailed description)</li>
<li>the version must not end in -SNAPSHOT (more on that later)</li>
<li>license information</li>
<li>developers information, i.e. who is contributing to the project</li>
<li>source code management information (basically, the link to the git repository)</li>
</ul>

You can see the POM of my project <a href="https://github.com/ngeor/archetype-quickstart-jdk8/blob/master/pom.xml" target="_blank">here</a>, to get an idea of the elements mentioned above. This is however the easy part. You just need to fill this information in. Note that publishing to Nexus will fail if these are missing, but it will let you know what you're missing, which is helpful.

Getting the javadoc and the source in the jar is also easy. You just need to configure two maven plugins: <code>maven-javadoc-plugin</code> and <code>maven-source-plugin</code> respectively.

The more difficult part is the <strong>GPG signing</strong>, because it has some overhead. On my Windows laptop, I found the <code>gpg</code> command line utility bundled with my Git Bash installation, so that's good. The principle is the usual: you need to generate a key pair (public / private). You publish the public key on a public server (so that Nexus can retrieve it). You sign the artifacts with the private key. Nexus is able to verify this way that the owner of the private key (you) published these artifacts.

It gets a bit more complicated, because the signing of the artifacts will be performed by Travis. This means that I will need to store the private key in my source code so that Travis can read it. Now, the private key is called private for a reason. If I store it as-is, anyone with access to the code can impersonate me. In general, storing passwords and similar things in the code is a bad idea, not only for open source repositories, but for private code as well. To mitigate the risk, I used gpg to <strong>encrypt the key</strong> and store it in git encrypted. It can only be used with a passphrase, which I store in git as an <strong>encrypted environment variable</strong> (a feature Travis supports). The actual signing is done by yet another maven plugin: <code>maven-gpg-plugin</code>.

One more thing which revolves around CI is the <strong>version</strong>. Semantic versioning is encouraged for library projects. I like to use this approach: I define the major and minor components of the version and I let the CI provide the patch number. So I control the "1.0." part and Travis provides the final "2", to form a version like "1.0.2". This way I have an automatically incrementing version effortlessly, while I can still define what constitutes a breaking change when I need to. Setting the version is a simple text replace in the pom using <code>sed</code>.

If we have all this in place, we can publish to nexus with no extra plugin. Maven calls this the "deploy phase" in the "life-cycle". It has a built in concept that the artifact's final destination in its life is to be published in such a repository. This rigid life-cycle is not my favorite part of Maven, but that's a discussion for another time. All we need is to define where we're publishing (OSSRH) by using the <code>distributionManagement</code> element in the POM. And finally, specify the credentials (those JIRA credentials) in a custom <code>settings.xml</code> file for Maven. Just like with the private key, it's best to use an encrypted environment variable in Travis. In TeamCity, you would use a password parameter.

If you manage to get through all this, you'll have a new package. You might thing we're done. Well, sorry, no. Unfortunately, it doesn't get published directly, but it ends up in a <strong>staging area</strong> where you can review it, approve it or reject it. Like I said, the whole experience feels a bit antiquated. This is one last bit that needs manual intervention unfortunately. It looks like this:

<img src="{{ site.baseurl }}/assets/2017/03/27/11_32_33-nexus-repository-manager.png" />

You need to first "Close" and then "Release" the package. You can also browse to verify it has the expected version:

<img src="{{ site.baseurl }}/assets/2017/03/27/11_33_24-nexus-repository-manager.png" />

The first time you publish, you need to comment on the JIRA ticket, so that they will set up some synchronization process. This is a one time only task. Once that is done, the package finally becomes available. Subsequent deployments don't require any JIRA interaction.

Due to the manual review step, it's <strong>not possible</strong> to fully automate the process until having the package live. It is still possible to go from committing code up to having a Maven package pending for review with no manual intervention.

Compared with npm and NuGet, this is a very difficult process. What I expect from this kind of service:
<ul>
<li>friendly UI, mobile friendly as well</li>
<li>simple signup process should suffice to be able to publish</li>
<li>able to go live with no manual intervention</li>
</ul>

I hope they start looking at what other platforms are doing and improve this experience, as well as their Nexus UI which could use a makeover.

One last bit left: <strong>celebrate</strong>! Celebrate that our new package is there for the whole world to use! And what better way to celebrate than to add a <a href="{{ site.baseurl }}/2016/03/05/github-badges.html">badge</a> to your repository's README to show off the maven package and its version! That's done with this nice <a href="https://github.com/jirutka/maven-badges" target="_blank">project that makes maven badges</a>.
