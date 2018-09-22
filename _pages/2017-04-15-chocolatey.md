---
layout: page
title: Chocolatey
date: 2017-04-15 08:24:37.000000000 +02:00
type: page
parent_id: '0'
published: true
categories: []
tags: []
author: Nikolaos Georgiou
---
<p>Chocolatey is a package manager for Windows. In this page, I keep track of packages I'm using for future reference.</p>
<p>I use a custom install location for Chocolatey. At home: C:\opt\chocolatey and at work C:\ecommerce\chocolatey (due to IT policy restrictions). This is defined in the environment variable ChocolateyInstall.</p>
<p><img class="alignnone size-medium wp-image-1743" src="{{ site.baseurl }}/assets/2017-04-15-10_37_12-clipboard.png?w=600" alt="2017-04-15 10_37_12-Clipboard" width="300" height="78" /></p>
<p><a href="https://chocolatey.org/install" target="_blank">Installation cheat sheet</a> (needs Powershell as Admin):</p>
<p>[code]</p>
<p>Set-ExecutionPolicy RemoteSigned</p>
<p>iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))</p>
<p>[/code]</p>
<p>Packages I use:</p>
<ul>
<li>7zip
<ul>
<li>Installs in C:\Program Files\7-Zip</li>
</ul>
</li>
<li>baretail
<ul>
<li>Portable, installs in C:\opt\chocolatey\lib\baretail\tools</li>
</ul>
</li>
<li>keepassx
<ul>
<li>Portable, installs in C:\opt\chocolatey\lib\keepassx\tools\KeePassX-2.0.3</li>
</ul>
</li>
<li>maven (installs jdk8 too)
<ul>
<li>Need to set M2_HOME env variable to C:\opt\chocolatey\lib\maven\apache-maven-3.3.9</li>
</ul>
</li>
<li>mysql.workbench</li>
<li>notepadplusplus</li>
<li>python (installs python3)</li>
</ul>
