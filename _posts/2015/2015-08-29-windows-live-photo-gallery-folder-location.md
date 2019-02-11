---
layout: post
title: Windows Live Photo Gallery Folder Location
date: 2015-08-29 05:40:00.000000000 +02:00
published: true
categories:
- my-computer
tags: []
---

If, for whatever reason, you want to force Windows Live Photo Gallery to rebuild its database, you can just delete the folder where it stores its settings. The folder location is:

```
%userprofile%AppDataLocalMicrosoftWindows Live Photo Gallery
```

after deleting this, it will rebuild thumbnails, read metadata, perform face recognition, the whole thing.
