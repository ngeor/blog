---
layout: post
title: 'Tip: Windows PowerShell and OneDrive'
date: 2017-04-16 11:57:09.000000000 +02:00
published: true
tags:
- OneDrive
- Windows PowerShell
---

If your Windows PowerShell profile is inside your OneDrive folder and you don't like that, this is what you have to do:<!--more-->
<ul>
<li>open the Registry Editor</li>
<li>navigate to HKEY_CURRENT_USER, SOFTWARE, Microsoft, Windows, CurrentVersion, Explorer, User Shell Folders</li>
<li>change the Personal key's value</li>
</ul>

<img src="{% link /assets/2017/04/16/13_51_21-registry-editor.png %}" />

In this example, the old value of the Personal folder was C:\Users\ngeor\OneDrive\Documents. This is what Windows PowerShell uses to determine where the profile should live. Changing this to the non-OneDrive old school "My Documents" folder (C:\Users\ngeor\Documents in my case) works for PowerShell too.

Of course, the impact is that all applications will now think that the OneDrive location is not the default, so be aware of that.

References:
<ul>
<li><a href="https://blogs.technet.microsoft.com/heyscriptingguy/2012/05/21/understanding-the-six-powershell-profiles/" target="_blank">Understanding the Six PowerShell Profiles</a></li>
<li><a href="https://technet.microsoft.com/en-us/library/cc962613.aspx" target="_blank">User Shell Folders</a></li>
<li><a href="https://support.microsoft.com/en-us/help/931087/how-to-redirect-user-shell-folders-to-a-specified-path-by-using-profile-maker" target="_blank">How to redirect user shell folders to a specified path by using Profile Maker</a></li>
</ul>
