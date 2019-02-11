---
layout: post
title: Recording animated gifs in ubuntu
date: 2015-09-07 07:30:00.000000000 +02:00
published: true
categories:
- my-computer
tags: []
---

Last week I wanted to do a small screen recording on my Ubuntu desktop and save it as an animated gif. I tried <a href="https://screentogif.codeplex.com/">ScreenToGif</a> but that didn’t work in Ubuntu, it threw an exception when I pressed the record button. I found a good solution in this <a href="http://askubuntu.com/questions/107726/how-to-create-animated-gif-images-of-a-screencast">askubuntu</a> question and I'm building on top of it to make it as easy as right clicking on a video file.

## Overview and software required

There are three basic steps in this process:
<ul>
<li><strong>Make a video recording of the screen</strong>. You’ll need <code>gtk-recordmydesktop</code> to record the video. This is a quite user friendly desktop application.</li>
<li><strong>Convert the video to JPEG files</strong>. You’ll need <code>mplayer</code> to convert the video to JPEG image files.</li>
<li><strong>Convert the JPEG files into an animated GIF</strong>. You’ll need <code>imagemagick</code> to convert the JPEG images into a single animated GIF.</li>
</ul>

To install these tools, run:

<code>
sudo apt-get install imagemagick mplayer gtk-recordmydesktop
</code>
<h2 id="record-the-video">Record the video</h2>

No command line kung-fu is required for this one, which is something I can’t say for the next steps. Just start the RecordMyDesktop app (installed earlier with <code>gtk-recordmydesktop</code>) and record the video. It stores it in the ogv format.
<h2 id="convert-to-jpegs">Convert to JPEGs</h2>

In this part, we use <code>mplayer</code> to convert the video to JPEG images. From a command line:

```
mplayer -ao null <video file name> -vo jpeg:outdir=output
```

This command will convert the video into a series of JPEG image files and it will store them in a folder called output.
<h2 id="convert-to-animated-gif">Convert to animated GIF</h2>

Here we convert the JPEG images into a single animated GIF file. Run the following command:

```
convert output/* output.gif
```

<h2 id="optimizing-the-gif">Optimizing the GIF</h2>

If you run the above, you’ll notice that the file size of the GIF may be a bit too large to be put on a web page.

There’s two things you can do:
<ol>
<li>Animation Optimization</li>
<li>Resize the source JPEG images in advance</li>
</ol>
<h3 id="animation-optimization">Animation Optimization</h3>

ImageMagick has some built-in capabilities that go a long way optimizing the final file size of the GIF file. To optimize an animated GIF, try out this command:

```
convert output.gif -fuzz 10% -layers Optimize optimised.gif
```

If you want to read more about it:
<ul>
<li><a href="http://www.imagemagick.org/Usage/anim_opt/">Animation Optimization</a></li>
<li><a href="http://www.imagemagick.org/Usage/color_basics/#fuzz">The fuzz factor</a></li>
</ul>
<h3 id="resize-the-source-jpeg-images">Resize the source JPEG images</h3>

You can scale down the JPEG images without sacrificing too much readability. To convert a single JPEG file, you can use ImageMagick again:

```
convert in.jpg -resize -resize 440x330 out.jpg
```

Since we have a bunch of files, some bash scripting will be needed:

```sh
#!/bin/bash

# input folder
IN="$1"

# output folder
OUTPUT="$IN-resized-440w"

mkdir $OUTPUT
for i in $(find $IN -type f); do
	o=$OUTPUT/$(basename "$i")
	convert $i -resize 440x330 $o
done
```

This script takes a JPEG folder as input and creates a new folder with all images resized.
<h2 id="putting-it-all-together">Putting it all together</h2>

I like <a href="https://help.ubuntu.com/community/NautilusScriptsHowto">Nautilus scripts</a> and I think it would be great to just be able to right click on a video, “Convert to Animated GIF”, done (well it takes a while to do all the processing, but still).

The following is a rather naive version of such a script:

```sh
#!/bin/bash

# input file
VIDEO="$@"

# output file
OUTPUT="$@.gif"

# temporary folder
TMP=/tmp/convert-video-to-gif/

# temporary folder for jpegs
TMP_JPEG=$TMP/output/

TMP_UNOPTIMIZED_GIF=$TMP/unoptimized.gif

# create folder
rm -rf $TMP
mkdir $TMP

mplayer -ao null "$VIDEO" -vo jpeg:outdir=$TMP_JPEG
convert $TMP_JPEG/* $TMP_UNOPTIMIZED_GIF
convert $TMP_UNOPTIMIZED_GIF -fuzz 10% -layers Optimize $OUTPUT

zenity --info --text="Finished converting $VIDEO, result is at $OUTPUT"
```

Note that it uses <a href="https://help.gnome.org/users/zenity/stable/">zenity</a> to display an info message when it’s all done.

This script will take the video <code>my-video.ogv</code> and convert it into an animated GIF named <code>my-video.ogv.gif</code>. But be aware:
<ul>
<li>it has no sanity checks</li>
<li>it won’t work with filenames that contain spaces</li>
<li>it doesn’t do the JPEG resizing part</li>
</ul>

Next time I’ll need an animated GIF, I might get around to writing it a bit better.
