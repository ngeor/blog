---
layout: post
title: Installing Ruby and Ruby on Rails on IIS - Doesn't work
date: 2010-11-17 11:41:00.000000000 +01:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

I tried to see if it's possible to install the latest Ruby on Rails on IIS 7.0. I didn't manage to do it and the reason is that there is something broken in the fast cgi ruby gem.
<h2>Installing Rails</h2>

Installing Rails itself is a pretty straightforward process. For Ruby, there is a separate installer for Windows available <a href="http://rubyinstaller.org/downloads/" target="_blank">here</a>. From there, installing Rails is done as usual with the gem command "gem install rails".

I also installed the SQLite gem (sqlite3-ruby). On the Mac, that required a native extension to be built (which means that the system must have some sort of C/C++ build environment that can play with configure and make). On Windows however, that is rarely the case. The people who package the SQLite gem know about this and I got this friendly screen:

```
C:Documents and SettingsAdministratorDemoApp>gem install sqlite3-ruby
=============================================================================
You've installed the binary version of sqlite3-ruby.
It was built using SQLite3 version 3.7.3.
It's recommended to use the exact same version to avoid potential issues.

At the time of building this gem, the necessary DLL files where available
in the following download:

http://www.sqlite.org/sqlitedll-3_7_3.zip

You can put the sqlite3.dll available in this package in your Ruby bin
directory, for example C:Rubybin
=============================================================================
Successfully installed sqlite3-ruby-1.3.2-x86-mingw32
1 gem installed
Installing ri documentation for sqlite3-ruby-1.3.2-x86-mingw32...
Installing RDoc documentation for sqlite3-ruby-1.3.2-x86-mingw32...
```

This is fantastic. The gem gets successfully installed and on the output I get perfect instructions on where to get the dlls and where to place them.

At this point, I have a working rails installation with SQLite support.
<h2>Trying to run Rails from IIS</h2>

That's where it got complicated. I gave it a brave fight but at the end I gave up. The idea is that IIS and Ruby will talk together via FastCGI and the steps required to make the magic work are the following:
<ul>
<li>We need a URL Rewriter so that the SEO friendly URLs of Rails will be intercepted. IIS has a <a href="http://www.iis.net/download/URLRewrite" target="_blank">URLRewrite module</a> that does the trick.</li>
<li>We need a FastCGI module for IIS that will call Ruby to handle the request. IIS has a module for that too, the FastCGI module. For IIS 7, this is built-in, but you need to select the CGI feature in IIS features. However, this doesn't install the support to manage FastCGI in the IIS Management Console. There's a <a href="http://www.iis.net/download/AdministrationPack" target="_blank">separate install called the Admin Pack</a> for that. Note that a lot of tutorials out there are quite old and refer to third party tools for URL Rewriting and FastCGI on IIS.</li>
<li>We need a Ruby dispatcher script that will handle the request. That's the script that IIS FastCGI module will call. In the previous version of rails, there was a dispatch.fcgi file on the public folder. That file is now gone. Searching around, which was not very easy because most of the links are for Rails 2, I figured out that there's a new Web system in Rails, called Rack, which supports all sorts of things, FastCGI being one of them. I also found a <a href="http://forum.alwaysdata.com/viewtopic.php?pid=7230" target="_blank">sample dispatch.fcgi for Rails 3</a> that uses that Rack thing.</li>
</ul>

In theory, we are ready to go! In practice, we fail at the FastCGI gem...

The <a href="http://rubygems.org/gems/fcgi" target="_blank">FastGCI gem</a> requires a native extension to be build and, unlike the SQLite people, there are no precompiled binaries for the <a href="http://www.fastcgi.com/" target="_blank">FastCGI library</a>.

I spent a lot of fun hours setting up a MinGW environment to try to compile FastCGI natively, only to figure out that they don't really support MinGW and I should use Visual Studio 6 ( ! ). I did that ( !! ) and it worked. I had a FastCGI dll. I copied the dll and the header files to folders where Rails could find it and... the gem wouldn't build. The FastCGI gem was using in its C code some flag (FL_GETFL I believe it was) that is not supported in Windows environments...

That's where I gave up, convincing myself that the FastCGI people are not testing these things on Windows.

It seems that most of the Ruby on Rails people are on Linux or Mac anyway. For Windows, there's always Apache that you can use I guess. But I think it shouldn't be that difficult. PHP on IIS works with FastCGI for some time now. From the results that I found searching, most of them where from IIS Blogs and not from Ruby on Rails people, which I think shows that the RoR community, well, let's say that IIS support is not their first priority.

Another very useful post was <a href="http://blogs.iis.net/ruslany/archive/2008/08/07/ruby-on-rails-in-iis-7-0-with-url-rewriter.aspx" target="_blank">this one</a>, but again it's from 2008. The steps are more or less the same and the concept of how to connect all the components together (URLRewrite, FastCGI, Ruby FastCGI Dispatcher script, Rails application) is the same but that is now broken for Rails 3 because of the FastCGI gem. I think they should follow the SQLite example and make it easy on the users.
