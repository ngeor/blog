---
layout: post
title: Combine subversion post-commit hooks with NAnt
date: 2010-07-25 10:08:00.000000000 +02:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

Subversion offers a mechanism called <a href="http://svnbook.red-bean.com/en/1.4/svn.ref.reposhooks.post-commit.html">post-commit</a> hook that allows an executable file to be run on the subversion server after a successful commit has been made. Since I host my own home server, containing both this website and my own subersion server, I thought I could use this mechanism to automatically update some files on the website when a commit has been made. For example, if I commit some changes on a web page template, it would be nice if it would automatically be updated on the website and also be packaged as a zip file for visitors of the site to download.

To make it a bit simpler at first, I want a post-commit hook on a repository that will get the latest version after the commit and copy certain files to a certain folder. From time to time, I would like to modify that list of files. Now, the executable that can be run in the post-commit hook can be an .exe or a .bat file. An .exe file doesn't seem right, because it's tedious to update an .exe file everytime I want to modify the list of files I want to copy. The batch file is a better alternative but, and this applies also to the .exe solution, being a hook it means that it will not live inside the repository. Therefore, I would have to modify the batch file separately before every commit that changes the list of files to be copied. And I will have to open up remote access of some sort to the hooks folder of the subversion server in order to do so. That doesn't seem right either. Wouldn't it be nice if my source code also describes the post-commit actions? So I need to find a way to bring the control of the post-commit actions inside my source tree. That's where I though I can use NAnt.

The idea is that the post-commit hook will be really minimal and do only the following actions:
<ol>
<li>Create a temporary folder</li>
<li>Export the latest source code into the folder</li>
<li>Run NAnt specifying a special target name, e.g. postcommit</li>
<li>Delete the temporary folder</li>
</ol>

And the real set of actions to be performed will be defined as a NAnt build script in the root of my source tree, using a predefined target name (e.g. postcommit). I find this approach more generic and powerful. In effect, we are converting our subversion server into a powerful tool that can do whatever NAnt allows: automatic build, automatic unit-testing and continuous integration, e-mail reports, backup, whatever. As long as you can specify it in a NAnt build file, the subversion server will run it.

This is how my post-commit hook looks like:

```
REM Create Temp folder
mkdir c:Temp
cd C:Temp

REM Export source code into trunk folder
"C:Program FilesSubversionbinsvn" export
  --username myusername
  --password mypassword
  svn://svnhost/repository/trunk
  trunk

REM Go into trunk folder
cd C:Temptrunk

REM Run NAnt
"C:Program Filesnant-0.90binnant" postcommit

REM Cleanup
cd C:Temp
del /f /q/ s trunk
rmdir /q /s trunk
```

and this is a sample of a NAnt file:

```
<?xml version="1.0"?>
<project name="demo" default="postcommit" basedir=".">
	<description>demo autodeploy script</description>
	<property name="dest.dir" value="C:/Web" overwrite="false" />
	<target name="postcommit" description="">
		<touch file="${dest.dir}/it_worked.txt" />
	</target>
</project>
```

If you noticed the full paths in the post-commit batch file, that's because post-commit hooks run in an empty environment, which also means empty PATH variable. Also, it assumes that there's a trunk folder in your source tree and that folder contains a NAnt build file which has a target called postcommit. The trunk folder should exist, if you use the recommended root folder structure for the subversion repositories (trunk, branches, tags). So, if you copy the post-commit hook into the hooks folder of your repository on every commit NAnt will kick in and execute your custom actions. The sky is the limit! Hope this helps.
