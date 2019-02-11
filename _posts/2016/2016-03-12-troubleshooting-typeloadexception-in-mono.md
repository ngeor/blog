---
layout: post
title: Troubleshooting TypeLoadException in mono
date: 2016-03-12 06:59:35.000000000 +01:00
published: true
categories:
- programming
tags:
- ".NET"
- mono
- troubleshooting
- TypeLoadException
---

I don't do a lot of .NET programming these days. At work we deal mostly with
JavaScript. However, C# is still the language I'm more fluent in and, also
important, a language that I really like. That's why sometimes I like to code a
bit in C# at home. That can be either on Windows or on a Mac with Mono. The
problem with Mono is that things can always be a bit different and require some
extra effort.

This time I am working on a project that downloads your entire Google Drive
locally. The twist is that it automatically converts Google Docs/Sheets/etc into
their Microsoft (or OpenOffice) counterpart formats. That's not what Google
Drive does. With Google Drive, these files are stored locally as small JSON
files, mere pointers to the data in the cloud. If you want to be a bit more in
control of your data, but you don't want to setup your own cloud, maybe a
periodic export to concrete formats like docx is the answer.

Anyway, back to my Mono problems. The project was running fine on Windows, but
on my Mac (mono 4.2.3) I ended up in a TypeLoadException:

```
$ mono GoogleDriveOfflineBackup.CLI.exe

Unhandled Exception:
System.TypeLoadException: Could not load type 'Google.Apis.Drive.v3.DriveService' from assembly 'Google.Apis.Drive.v3, Version=1.10.0.13, Culture=neutral, PublicKeyToken=4b01fa6e34db77ab'.
  at GoogleDriveOfflineBackup.CLI.Program.Main (System.String[] args) <0x6b4f70 + 0x00027> in <filename unknown>:0
[ERROR] FATAL UNHANDLED EXCEPTION: System.TypeLoadException: Could not load type 'Google.Apis.Drive.v3.DriveService' from assembly 'Google.Apis.Drive.v3, Version=1.10.0.13, Culture=neutral, PublicKeyToken=4b01fa6e34db77ab'.
  at GoogleDriveOfflineBackup.CLI.Program.Main (System.String[] args) <0x6b4f70 + 0x00027> in <filename unknown>:0
```

It's complaining about a DLL from Google Drive API, but that DLL is definitely
in the correct folder and it is definitely the correct version.

In this case, the problem lies with a dependency of a dependency. To
troubleshoot it, you have to invoke mono in a special way. If you run the same
command with the environment variable MONO_LOG_LEVEL set to debug, you'll get a
much longer output. Somewhere close to the end you'll find the real culprit:

```
$ MONO_LOG_LEVEL=debug mono GoogleDriveOfflineBackup.CLI.exe
[...]
Mono: The following assembly referenced from Google.Apis.Core.dll could not be loaded:
     Assembly:   System.Net.Http    (assemblyref_index=5)
     Version:    1.5.0.0
     Public Key: b03f5f7f11d50a3a
The assembly was not found in the Global Assembly Cache, a path listed in the MONO_PATH environment variable, or in the location of the executing assembly.

Mono: Failed to load assembly Google.Apis.Core[0x796886a0]

Mono: Could not load file or assembly 'System.Net.Http, Version=1.5.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a' or one of its dependencies.
[...]
```

So the missing library is actually System.Net.Http version 1.5.0.0. That's more
useful. Poking around in the project's references in Xamarin Studio, I was able
to see that it already uses System.Net.Http, but version 4.0.0.0. To use that,
we'll need a binding redirect in the app.config:

```
<?xml version="1.0" encoding="utf-8"?>
<configuration>
    <startup>
        <supportedRuntime version="v4.0" sku=".NETFramework,Version=v4.5" />
    </startup>
  <runtime>
    <assemblyBinding xmlns="urn:schemas-microsoft-com:asm.v1">
      <dependentAssembly>
        <assemblyIdentity name="System.Net.Http" publicKeyToken="b03f5f7f11d50a3a" culture="neutral" />
        <bindingRedirect oldVersion="0.0.0.0-4.0.0.0" newVersion="4.0.0.0" />
      </dependentAssembly>
    </assemblyBinding>
  </runtime>
</configuration>
```

And that workaround makes the project work again in Mono. Hope this helps!
