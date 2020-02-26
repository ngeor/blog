---
layout: post
title: Correcting EXIF dates on photos
date: 2016-01-30 14:01:45.000000000 +01:00
published: true
categories:
- tech
tags:
- exiftool
- metadata
- organization
- photos
---

Sometimes, the photos I take with my phone don't have the correct EXIF tags set. This gets annoying because those tags are used by photo organizers to determine when a photo was taken. If the photo doesn't contain the date in the EXIF tag, the organizer application will use the file's timestamp, which could change if you copy paste the file, move it around, move it to another computer, restore it from a backup and so on.<!--more-->

There's a nice command line utility, called <a href="http://www.sno.phy.queensu.ca/~phil/exiftool/" target="_blank">exiftool</a>, which is like a swiss army knife when it comes to manipulating these EXIF tags. I wrote a small python script that can be used to create these tags, provided that the date information is captured by the filename of the photo. For instance, if the photo file is named 'IMG_20160130_135210.jpg', then the python script can extract the date and time and tell exiftool to correct it.

I uploaded the script as <a href="https://gist.github.com/ngeor/dbcae5002d81b22b4466" target="_blank">a gist in GitHub</a>, it assumes exiftool is already installed and available on the PATH.

On Mac/Linux, you can run it as:

```
python fix-img-date.py IMG*.jpg
```

On Windows I think I had ran into some problems, so you can use Powershell to run it like this:

```
ls IMG*.jpg | % { python fix-img-date.py $_ }
```

Another cool thing I use exiftool for is to have consistent filenames for my photos. I prefer renaming them so that they just contain the date and time, in an almost ISO pattern, so when you sort by filename you also sort by time.

To rename a bunch of photos like that, they have to first have correct EXIF tags. Then, you can run:

```
exiftool "-FileName<DateTimeOriginal" -d "%Y-%m-%d %H%M%S.%%e" CAM*
```

and all the CAM* photos get renamed to names like "2016-01-30 140050.jpg"

Hope this helps!
