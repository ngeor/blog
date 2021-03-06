---
layout: post
title: Overriding EPiServer pages
date: 2011-07-21 19:20:00.000000000 +02:00
published: true
tags:
  - EPiServer
  - ".NET"
  - C#
---

It is not very frequent or pretty but still sometimes it’s inevitable: we have
to “steal” the code of EPiServer through
<a href="http://reflector.red-gate.com/" target="_blank">Reflector</a>/<a href="http://wiki.sharpdevelop.net/ILSpy.ashx" target="_blank">ILSpy</a>/other
and modify it to suit our needs. This way you can customize pages or user
controls anyway you wish, beyond the way EPiServer allows through conventional
channels.

The process is simple. Through Reflector or ILSpy you "steal" the code of the
page you want to override. You compile that class, with a different namespace,
into a new assembly. Then, you modify the markup file to point to your new
class. That's it.

Let's see an example, let's say you want to customize the NewPage.aspx that
EPiServer provides. What would you do:

<ol>
<li>Open NewPage.aspx in a text editor to figure out what class it inherits from ( e.g. <em>EPiServer.UI.Edit.NewPage</em> )</li>
<li>Open the assembly that contains that class in Reflector or ILSpy ( typically the assembly is EPiServer.UI.dll - at least for EPiServer 5 that I'm currently using )</li>
<li>Find the class and save it into a C# code file.</li>
<li>Edit this class in a text editor and change the namespace.</li>
<li>Compile this class into a new assembly and copy the assembly in EPiServer's installation bin folder.</li>
<li>Edit NewPage.aspx and change the class it inherits from, setting it to your new class.</li>
</ol>

At this point, the NewPage.aspx should still work but now the code is yours to
do as you please.

Hopefully you won't have to do many of these hacks. But regardless of that, you
should be careful on the maintenance of your code. An idea could be that you
keep all of these "stolen" classes in a separate assembly. Also you could mirror
the namespace structure of the classes you're "stealing", so if you're taking
the code from the class <em>EPiServer.UI.Edit.NewPage</em>, you can place its
copy at <em>MyProject.UI.Edit.NewPage</em>. This way of organizing the “stolen”
code offers the advantage that we know immediately the original location of the
class we “stole” from, in case we need to check back for the original. It also
removes the need of thinking where the “stolen” code should be placed and serves
as a straight forward convention for the developers to use.

Another good idea is to add comments in the code about all the things you change
and why you are doing it. These hacks should be justified and easy to isolate.
Otherwise upgrading to the next EPiServer version might become difficult. You
should know what your hacks do and why you implemented them in the first place;
maybe the next EPiServer version will have them as built-in features thus making
your hacks obsolete. And if you still need the hack, you should be able to
identify and isolate the customized part of the code in order to try and reapply
the hack in the next version.

Hope this helps.
