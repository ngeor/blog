---
layout: post
title: Installing Ruby on Rails on Windows 8
date: 2013-04-16 08:33:00.000000000 +02:00
published: true
categories:
- Code
tags: []
---

I had some problems installing Ruby on Rails on Windows 8 so I'm writing this down as a summary.

<strong>You might also want to read the <a href="/2013/08/installing-ruby-on-rails-august-2013">most recent post</a> on the same topic.</strong>
<ol>
<li>Use <a href="http://rubyinstaller.org/downloads/">RubyInstaller</a>. I recommend version 1.9.3. With version 2, I run into various problems trying to build native gems (e.g. libiconv not found). By default this will install Ruby at C:Ruby193. I also recommend selecting the Add Ruby to the PATH during installation, no need to do it manually later.</li>
<li>From the same site, download DevKit. It's a self extracting archive and you need to extract it to its final location. I extracted it under C:Ruby193devkit so it's together with ruby.</li>
<li>Install DevKit: from a command prompt, go to C:Ruby193devkit and run <code>ruby dk.rb init</code> and then <code>ruby dk.rb install</code></li>
<li>Update gem to latest and greatest with <code>gem update --system</code> and then <code>gem update</code></li>
<li>Install rails with <code>gem install rails</code></li>
<li>Install sqlite3 with <code>gem install sqlite3</code></li>
</ol>

So far so good. At this point we're ready to start going through the tutorial <a href="http://guides.rubyonrails.org/getting_started.html">Getting Started with Rails</a> to create our first application. Let's to that with the command <code>rails new blog</code>.

Among other things in the output, you'll notice that some gems are already present (e.g. json, rails) while others are being installed at that moment (e.g. execjs, coffee-script).

```
Installing coffee-script-source (1.6.2)
Installing execjs (1.4.0)
Installing coffee-script (2.2.0)
Using rack-ssl (1.3.3)
Using json (1.7.7)
Installing rdoc (3.12.2)
Using thor (0.18.1)
Using railties (3.2.13)
Installing coffee-rails (3.2.2)
Installing jquery-rails (2.2.1)
Using rails (3.2.13)
Installing sass (3.2.7)
Installing sass-rails (3.2.6)
Using sqlite3 (1.3.7)
Installing uglifier (2.0.1)
Your bundle is complete!
```

We can run the application at this point with <code>rails server</code> and indeed it will load the default index.html. Following the tutorial, we can create our first home controller and delete the index.html. The command to do that is <code>rails generate controller home index</code>. You also need to delete index.html and setup home#index as the default route.

This is where I had most of the problems. Instead of seeing my hello world message in this very simple controller, I ended up with the following error message in the command prompt:

```
Completed 500 Internal Server Error in 208ms

ActionView::Template::Error (
  (in C:/Users/nikolaos/Projects/blog/app/assets/javascripts/home.js.coffee)):
    3: <head>
    4:   <title>Blog</title>
    5:   <%= stylesheet_link_tag    "application", :media => "all" %>
    6:   <%= javascript_include_tag "application" %>
    7:   <%= csrf_meta_tags %>
    8: </head>
    9: <body>
  app/views/layouts/application.html.erb:6:in `_app_views_layouts_application_html_erb___564660063_19500504'

  Rendered C:/Ruby193/lib/ruby/gems/1.9.1/gems/actionpack-3.2.13/lib/action_dispatch/middleware/templates/rescues/_trace
.erb (1.0ms)
  Rendered C:/Ruby193/lib/ruby/gems/1.9.1/gems/actionpack-3.2.13/lib/action_dispatch/middleware/templates/rescues/_reque
st_and_response.erb (1.0ms)
  Rendered C:/Ruby193/lib/ruby/gems/1.9.1/gems/actionpack-3.2.13/lib/action_dispatch/middleware/templates/rescues/templa
te_error.erb within rescues/layout (11.0ms)
```

And this is the error message that the browser showed:

```
 ExecJS::RuntimeError in Home#index

Showing C:/Users/nikolaos/Projects/blog/app/views/layouts/application.html.erb where line #6 raised:

  (in C:/Users/nikolaos/Projects/blog/app/assets/javascripts/home.js.coffee)

Extracted source (around line #6):

3: <head>
4:   <title>Blog</title>
5:   <%= stylesheet_link_tag    "application", :media => "all" %>
6:   <%= javascript_include_tag "application" %>
7:   <%= csrf_meta_tags %>
8: </head>
9: <body>

Rails.root: C:/Users/nikolaos/Projects/blog
Application Trace | Framework Trace | Full Trace

app/views/layouts/application.html.erb:6:in `_app_views_layouts_application_html_erb___564660063_19500504'
```

Not very descriptive and a bit disappointing that the hello world tutorial doesn't "just work". The error has something to do with CoffeeScript, since the file it complains about is home.js.coffee. CoffeeScript is a nice little language that compiles into Javascript. Rails comes with out of the box support for this (or at least it claims it does). It uses ExecJS, another gem, to compile CoffeeScript into Javascript. ExecJS relies on the presence of a Javascript runtime in order to be able to do that. A lot of people suggested to bypass this problem by "simply installing node.js". However, <a href="https://github.com/sstephenson/execjs">ExecJS says that on Windows it just uses Microsoft Windows Script Host</a>. So I decided to keep on searching for a solution. After some more digging I found a <a href="https://github.com/sstephenson/execjs/issues/81">thread claiming that this problem is specific to Windows 8</a> and the solution is to modify ExecJS's code... scary to say the least and, again, very disappointing experience but it did the trick.

You have to modify the file runtimes.rb (assuming you've kept the default paths, it is under C:Ruby193librubygems1.9.1gemsexecjs-1.4.0libexecjs) and find the block that declares the JScript external runtime (that's Microsoft Windows Script Host) and change it into this:

```
JScript = ExternalRuntime.new(
  :name        => "JScript",
  :command     => "cscript //E:jscript //Nologo",
  :runner_path => ExecJS.root + "/support/jscript_runner.js",
  :encoding    => 'UTF-8'
)
```

After this change, my hello world controller worked. I've tried the above procedure in both Windows 8 32 and 64 bits. I was also able to follow the tutorial a bit more by generating the post scaffold and I didn't run into any problems with sqlite, it seems to work. I stopped at the point where he adds a second model, so I don't know if there are any further pitfalls ahead...
