---
layout: post
title: Android SDK with Jenkins
date: 2017-08-31 07:19:30.000000000 +02:00
published: true
tags:
- android
- Jenkins
---

In this post I'm setting up a Jenkins server to be able to package and sign Android packages. This is done on a 64bit PC running Ubuntu 14.04 (trusty).

<!--more-->

First of all, download the latest command line tools. You can find them on <a href="https://developer.android.com/studio/index.html" target="_blank" rel="noopener">this page</a> all the way at the bottom ("Get just the command line tools"):

<img src="{% link /assets/2017/android-sdk-download.png %}" />

You need to download that zip file and transfer it to the Jenkins server. You can also right click, copy the <a href="https://dl.google.com/android/repository/sdk-tools-linux-3859397.zip" target="_blank" rel="noopener">download URL</a>, and download it directly on the Jenkins server with wget or curl:

```
wget https://dl.google.com/android/repository/sdk-tools-linux-3859397.zip
```

Create a folder where you want the SDK to live, e.g. <code>/opt/android</code>. That folder needs to be writable by you and by Jenkins. You need to be able to write so that you'll unzip and accept licenses later. Jenkins needs to be able to write so that it'll be able to download the appropriate build tools automatically. For that purpose I've created a group that both my account and the jenkins user belong to. You can also just impersonate the jenkins user all along this process.

Unzip the downloaded archive in <code>/opt/android</code>. The next step is to accept the various licenses to be able to use the SDK. Go to <code>/opt/android/tools/bin</code> and run the <code>sdkmanager</code>:

```
cd /opt/android/tools/bin
./sdkmanager --licenses
```

It will present you various licenses that I'm pretty sure we all read thoroughly.

Next step is to install some 32bit libraries. If your build hangs inexplicably when merging PNG resources, it's probably missing this bit:

```
sudo apt-get install lib32stdc++6 lib32z1
```

After that, create an environment variable to point to the Android SDK. Create a file named <code>android.sh</code> under directory <code>/etc/profile.d</code> :

```
export ANDROID_HOME=/opt/android
```

If Jenkins is already running, restart it so that it will pick up the new environment variable.

This should be enough for Jenkins to be able to use the SDK. Here's how my build configuration looks like:

<img src="{% link /assets/2017/android-jenkins.png %}" />

The first part is using Gradle to produce an unsigned APK in release configuration.

The second part is using the build tools to produce a signed APK ready for publishing to the play store. You can read more about that in the <a href="https://developer.android.com/studio/publish/app-signing.html" target="_blank" rel="noopener">documentation</a>. Simplified, it looks like this:

```
# align the apk
zipalign -v -p 4 app-release-unsigned.apk app-unsigned-aligned.apk

# sign it
apksigner sign --ks-pass pass:SuperSecret --ks SuperSecret.jks --out app-signed.apk app-unsigned-aligned.apk

# verify the signed apk
apksigner verify app-signed.apk
```

In reality, I'm using hard coded paths and inline passwords, which are definitely points for improvement. Also, the certificate "SuperSecret.jks" (which you need to have generated already) needs to be present on the Jenkins server.
