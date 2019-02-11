---
layout: post
title: Building wxWidgets on Mac
date: 2017-08-30 13:41:44.000000000 +02:00
published: true
categories:
- programming
tags:
- C Plus Plus
- mac
- Makefile
- wxWidgets
---

In this post, I'm building wxWidgets on a Mac from source. This is done on a very old MacBook running El Capitan.<!--more-->

Building wxWidgets on a Mac is not very difficult. First, you download the source code and extract to a location where you want to use it from. I didn't want to install it on a system directory, so I extracted it in my home folder (<code>~/src/wxWidgets</code>).

Documentation is provided in a txt file. I prefer to build a static library, so that the generated applications won't need the wxWidgets library installed or distributed. That's mentioned a bit late in the txt file. Create a folder like <code>~/src/wxWidgets/build-cocoa-static</code> and from there configure the installation with <code>../configure --disable-shared</code> (you can also pass <code>--enable-debug</code> to enable debugging). The <code>--disable-shared</code> will make the generated executables larger in size, but they will be independent.

After configure finishes, run <code>make</code> to build wxWidgets. This will take a while. You can also build demos and samples (e.g. <code>cd samples; make</code>).

Now you can also install wxWidgets so it's available system wide. That's done with <code>sudo make install</code> but I didn't want to do that. Instead, I added <code>~/src/wxWidgets/build-cocoa-static</code> to my PATH. This way, I don't pollute my system with files I won't know how to uninstall and I can maintain multiple versions of wxWidgets side by side.

The Makefiles that the samples are using are quite complex (to me at least). I think copying the minimal sample's Makefile might be a good starting point. I have created an even smaller Makefile that uses the <code>wx-config</code> utility. <code>wx-config</code> generated command line arguments for compilation tasks. For example:
<ul>
<li><code>wx-config --cxx</code> generates the compiler command that should be used (<code>g++</code> in this case, with some Mac specific arguments)</li>
<li><code>wx-config --cxxflags</code> generates the compiler arguments, such as the include directories where wxWidgets headers can be found and the appropriate preprocessor symbols</li>
<li><code>wx-config --libs</code> generates the linker arguments, i.e. the libraries that the application should be linked against.</li>
</ul>

Using these, a Makefile can look like this:

```

CXX=`wx-config --cxx`

all: wxhelloworld

wxhelloworld: wxhelloworld.o
    $(CXX) -o wxhelloworld wxhelloworld.o `wx-config --libs`

wxhelloworld.o: wxhelloworld.cpp
    $(CXX) -c -o wxhelloworld.o wxhelloworld.cpp `wx-config --cxxflags`

clean:
    rm *.o
    rm wxhelloworld

```

Hope this helps.
