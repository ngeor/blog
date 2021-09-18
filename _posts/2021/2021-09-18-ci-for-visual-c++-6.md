---
layout: post
title: CI for Visual C++ 6
date: 2021-09-18 06:02:01
tags:
  - continuous integration
  - C++
  - just for fun
  - TeamCity
  - Visual Studio 6
  - Visual C++ 6
  - VirtualBox
---

Some time ago, I thought of hacking on some really old
C/C++ code I had written. I have a VirtualBox image running
Windows 2000 and Visual Studio 6 (yes, that old). However,
I also wanted to be able to run the code in modern
Visual Studio 2019. Verifying that I haven't broken anything
means I would have to manually build my code on two different
IDEs. That's just boring. Instead, I hacked together a way of running
my build for both Visual Studio versions.

Normally, this would have been an easy task. Install TeamCity server.
Install one TeamCity agent on a machine that has Visual Studio 2019
and one agent on a machine that has Visual Studio 6. The problem is
that Windows 2000 is rather old, so you can't install TeamCity there
(or anything else for that matter, I've tried to install various
programming languages to total failure).

So the Visual Studio 2019 part is easy. I install TeamCity (both server and agent) on my laptop, define a job, done. For the Visual Studio 6 part, I needed to somehow mimic the work of a build agent, which is more or less the following:

- start the VM that has Visual Studio 6
- get the source code into the machine
- run the build
- get the build artifacts out of the machine
- stop the VM

You can go with variations regarding the lifecycle management
of the VM, e.g. just leave it running instead of shutting it down,
clone a new VM instead of reusing the same to achieve parallel
builds, etc. In my case, I just start and stop it per job,
as it's not too time consuming. I rely on TeamCity's shared resources
feature to ensure only one job can use that VM at any time.

Luckily, VirtualBox has a CLI (`VBoxManage.exe`) which supports
all needed operations:

- `startvm --type headless` to start the VM without having it pop up in my screen while I'm working.
- `controlvm poweroff` to turn off the machine and `snapshot restorecurrent` to fall back to the VirtualBox snapshot that brings the VM to the pristine state.
- `copyto` to copy files into the VM (the source code)
- `run` to run the build
- `copyfrom` to copy files out of the VM (the interesting files are the artifacts, exe and dll files, and the build log)

Of course, in practice I encountered more problems. First of all,
the `startvm` command returns immediately (if this was a real
machine, it returns as soon as you press the power button to turn
the machine on). I can't just start copying files into the VM yet,
Windows 2000 hasn't loaded. As a workaround, I used the `guestcontrol stat C:\` command in a wait loop. This command checks if the C:\ drive
exists in the VM. If it succeeds it means not only that Windows 2000
has loaded, but also the VirtualBox Guest Extensions are ready (which is what enables file transfers).

The second problem was that file tranfers were unpredicatable: sometimes they would fail, or time out. In the end, I figured out that
this had to do with how VirtualBox logs in into the VM. There is an
added cost for that log in operation. To solve that, I configured
Windows 2000 to automatically log in with my username and make sure I
use that same user for the file transfers. This way, it seems VirtualBox is smart enough to reuse the same session and everything goes smooth.

Running the build itself was a bit tricky, but it worked.
The command is something like `$MSDEV $SlnInGuest /OUT $BuildLogAbsolute /MAKE ALL /REBUILD`, where:

- `MSDEV` points to Visual Studio 6's CLI `"C:\Program Files\Microsoft Visual Studio\Common\MSDev98\Bin\MSDEV.COM"` (I think I had to use the .com instead of the .exe file...)
- `SlnInGuest` points to the solution file
- `BuildLogAbsolute` points to the build log file

The reason for capturing the log file is that I couldn't get the build
output to show directly in TeamCity. So instead I redirect it to a file, copy it out of the VM, and print it manually.

The exit code of MSDEV is fortunately returned by VirtualBox so I can indicate
if the build was successful or not, without having to do some more hacky stuff like searching for "ERROR" in the build log.

Overall, the approach worked and I never ended up in some unexpected
intermediate state where I had to go manually into the VM. I even configured TeamCity to publish the build status on GitHub. It is
kind of cool to see on GitHub "VC6 build passed" in 2021.
