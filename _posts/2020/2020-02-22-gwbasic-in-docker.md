---
layout: post
title: GW-Basic in Docker
date: 2020-02-22 06:31:09
categories:
  - hacking
tags:
  - GW-Basic
  - Docker
---

This is one of those just for fun projects, doing it to see if it can be done.
Can I put `GWBASIC.EXE` inside a Docker image?

[GW-Basic](https://en.wikipedia.org/wiki/GW-BASIC) first appeared in 1983 and
its last version, 3.23, was released in 1988.
[Docker](https://en.wikipedia.org/wiki/Docker_%28software%29) on the other hand
had its initial release in 2013. That's a 25 year difference. GW-BASIC ran on
[MS-DOS](https://en.wikipedia.org/wiki/MS-DOS) and I believe it was supported
for some time in [Windows](https://en.wikipedia.org/wiki/Microsoft_Windows). It
doesn't run on modern versions of Windows though:

![GW-Basic does not run on Windows 10](/assets/2020/2020-02-22-07_51_37-gw-basic-windows-10.png)

The only way to revive it is to use a DOS emulator like
[DOSBox](https://en.wikipedia.org/wiki/DOSBox). DOSBox is cross-platform, so it
also runs on Linux, which is the way into Dockerizing GW-Basic.

**Legal note**: to the best of my knowledge, GW-Basic is still under copyright,
so distributing a Docker image that contains `GWBASIC.EXE` wouldn't most likely
be legal.

## DOSBox

If you launch DOSBox, you'll notice that it opens up two Windows:

![DOSBox on Windows](/assets/2020/2020-02-22-08_02_24-dosbox-two-windows.png)

The one on the left is a standard console app. The one on the right looks like a
console app but it's actually rendering
[SDL](https://en.wikipedia.org/wiki/Simple_DirectMedia_Layer) graphics (DOSBox
can be used to emulate games too). Thinking about Docker and console
applications, the first window _might_ give us a chance to tap into the
[stdin/stdout streams](https://en.wikipedia.org/wiki/Standard_streams), while
the second one is just pixels. In fact, we want to prevent the second window
from appearing at all. With a bit of
[searching](https://duckduckgo.com/?t=ffab&q=dosbox+headless&ia=web), there is a
possibility to
[run DOSBox in a headless mode](https://superuser.com/questions/790519/running-dosbox-completely-headless)
by setting the environment variable `SDL_VIDEODRIVER` to `dummy`.

The next issue that we have is that DOSBox is an interactive program, which by
default just opens up its window and waits patiently for our commands. Let's see
what [command line options](https://www.dosbox.com/wiki/Usage) we can use. It
seems they have this use case figured out already:

`dosbox app -exit` will 1) mount the directory of `app` as the `C:` drive of
MS-DOS 2) run `app` 3) exit once it's done.

I will also use the `-noautoexec` flag because I already have a configuration
file on my laptop and I don't want it to interfere.

Now, we can't use `dosbox GWBASIC.EXE -exit` because GW-Basic is also
interactive. By default it just waits for the user to start entering Basic
commands. But `GWBASIC.EXE PROGRAM.BAS` will load and run the given Basic
program. Note that it still won't exit after running the program. For that to
happen, the program must explicitly use the `SYSTEM` command. Example:

```basic
10 PRINT "Hello, world!"
20 SYSTEM
```

If we don't have the `SYSTEM` command, the program won't exit. Additionally,
make sure that `PROGRAM.BAS` uses CRLF for
[line endings](https://en.wikipedia.org/wiki/Newline).

Since DOSBox can't pass parameters to the executable, we need a small batch file
for that.

Let's give this a try without Docker first.

I create a file `PROGRAM.BAS` in the same folder as `GWBASIC.EXE` with the same
contents as above (and, again, I make sure the line endings are CRLF). In the
same folder, I create a batch file `RUNGW.BAT` with contents
`GWBASIC.EXE PROGRAM.BAS`.

And from the command prompt let's try this:

`C:\> "C:\Program Files (x86)\DOSBox-0.74\DOSBox.exe" C:\Users\ngeor\DOSBOX\PROGS\GWBASIC\RUNGW.BAT -exit -noautoexec`

Well it all goes pretty fast and we get no output... to figure out what went
wrong, I remove the `-exit` flag:

![The output does not go to stdout](/assets/2020/2020-02-22-08_45_38-fail.png)

The batch file did its job, it launched GW-Basic with `PROGRAM.BAS` and exited.
But, the output is printed on the graphics window. Which kind of makes sense,
DOSBox just runs an emulation and it doesn't link its own stdout with whatever
is happening inside the emulation. And there does not seem to be any option in
the documentation that can move us further. It seems we've hit an obstacle.
[Shaka, when the walls fell](https://en.wikipedia.org/wiki/Darmok).

## Capturing stdout

Well, since we have that `RUNGW.BAT` batch file in place, we can use it to
capture the output of the program ourselves:

```bat
GWBASIC.EXE PROGRAM.BAS > STDOUT.TXT
```

The batch file is run inside the DOSBox emulation in the `C:` drive. So the
batch file will capture our "Hello, world!" message in `C:\STDOUT.TXT`, which
will be available outside the emulation in the same folder as everything else.
We now need a new wrapper script which runs DOSBox and then prints out
`STDOUT.TXT`.

```bat
@ECHO OFF
set SDL_VIDEODRIVER=dummy
"C:\Program Files (x86)\DOSBox-0.74\DOSBox.exe" C:\Users\ngeor\DOSBOX\PROGS\GWBASIC\RUNGW.BAT -exit -noautoexec
type C:\Users\ngeor\DOSBOX\PROGS\GWBASIC\STDOUT.TXT
```

I save this as `RunDOSBox.bat` and fire it up in a DOS prompt:

```bat
$ RunDOSBox.bat
Hello, world!
```

Victory!

Note that I used on purpose filenames in all capitals and in
[8.3 format](https://en.wikipedia.org/wiki/8.3_filename) if they are going to be
visible inside the DOS emulation (e.g. `RUNGW.BAT`) but not for outside (e.g.
`RunDOSBox.bat`).

## Dockerize it

Now, it's time to Dockerize. We need to convert `RunDOSBox.bat` into a bash
script and build a Dockerfile.

```Dockerfile
FROM ubuntu
RUN apt-get update \
    && apt-get install -y dosbox \
    && rm -rf /var/lib/apt/lists/*
ENV SDL_VIDEODRIVER=dummy
WORKDIR /app
COPY GWBASIC.EXE .
COPY *.BAT .
COPY *.BAS .
COPY *.sh .
CMD /app/run-dos-box.sh
```

```sh
#!/bin/sh
dosbox RUNGW.BAT -exit
cat STDOUT.TXT
```

If we build this with `docker build . -t gwbasic` and run it with
`docker run gwbasic` we see this output:

```
$ docker run gwbasic
ALSA lib confmisc.c:767:(parse_card) cannot find card '0'
ALSA lib conf.c:4528:(_snd_config_evaluate) function snd_func_card_driver returned error: No such file or directory
ALSA lib confmisc.c:392:(snd_func_concat) error evaluating strings
ALSA lib conf.c:4528:(_snd_config_evaluate) function snd_func_concat returned error: No such file or directory
ALSA lib confmisc.c:1246:(snd_func_refer) error evaluating name
ALSA lib conf.c:4528:(_snd_config_evaluate) function snd_func_refer returned error: No such file or directory
ALSA lib conf.c:5007:(snd_config_expand) Evaluate error: No such file or directory
ALSA lib pcm.c:2495:(snd_pcm_open_noupdate) Unknown PCM default
ALSA lib seq_hw.c:466:(snd_seq_hw_open) open /dev/snd/seq failed: No such file or directory
DOSBox version 0.74
Copyright 2002-2010 DOSBox Team, published under GNU GPL.
---
CONFIG: Generating default configuration.
Writing it to /root/.dosbox/dosbox-0.74.conf
CONFIG:Loading primary settings from config file /root/.dosbox/dosbox-0.74.conf
MIXER:Can't open audio: No available audio device , running in nosound mode.
ALSA:Can't open sequencer
MIDI:Opened device:none
SHELL:Redirect output to STDOUT.TXT
Hello, world!
```

There's a lot of output from DOSBox interfering with our hello world greeting,
which is visible as the last line. Let's modify the shell script to suppress
that:

```sh
#!/bin/sh
dosbox RUNGW.BAT -exit > /dev/null 2>&1
cat STDOUT.TXT
```

And finally, there it is:

```sh
$ docker run gwbasic
Hello, world!
```

## What we have so far

So, a summary of what we have:

- `PROGRAM.BAS`: a Basic program which prints "Hello, world!" and exits
  immediately
- `RUNGW.BAT`: a Windows batch file which runs `GWBASIC.EXE` with `PROGRAM.BAS`
  and redirects stdout to `STDOUT.TXT`
- `run-dos-box.sh`: a Bash script which runs DOSBox in headless mode with
  `RUNGW.BAT`, suppresses its output, and prints out `STDOUT.TXT` instead
- a Docker image which bundles everything together and runs `run-dos-box.sh`

## Executable Docker image

The Docker image works, but the program it executes is always the same
`PROGRAM.BAS`. If we want to change it, we will have to build a new Docker
image. It would be great if our Docker image could run any GW-Basic program,
without having to rebuild it every time.

We're modify the Dockerfile in the following way:

```Dockerfile
FROM ubuntu
RUN apt-get update \
    && apt-get install -y dosbox \
    && rm -rf /var/lib/apt/lists/*
ENV SDL_VIDEODRIVER=dummy
WORKDIR /app
VOLUME [ "/app/basic" ]
COPY GWBASIC.EXE .
COPY *.BAT .
COPY *.sh .
ENTRYPOINT ["/app/run-dos-box.sh"]
CMD ["PROGRAM.BAS"]
```

What has changed:

- The `PROGRAM.BAS` file is no longer copied into the image.
- There is a `/app/basic` folder defined as a volume. This is where `BAS` files
  will live. The user of the Docker image will be able to mount a directory
  containing the program(s) he/she wants to run.
- The image defines an entry point and a default command argument. This turns
  the image into an executable. Running `docker run gwbasic` will effectively
  run `/app/run-dos-box.sh PROGRAM.BAS` while running
  `docker run gwbasic NIBBLES.BAS` will effectively run
  `/app/run-dos-box.sh NIBBLES.BAS`.

Note that the name `PROGRAM.BAS` is still hard-coded in `RUNGW.BAT`. We can't
pass parameters to that batch file, because DOSBox does not support that (which
was the whole point why this batch file exists). Since our `RUNGW.BAT` will
always execute `PROGRAM.BAS`, we need to take care of that in the shell script
by copying the file in its expected location in advance:

```sh
#!/bin/sh
if [ ! -r "basic/$1" ]; then
    echo "File $1 not found"
    exit 1
fi

cp "basic/$1" PROGRAM.BAS
dosbox RUNGW.BAT -exit > /dev/null 2>&1
cat STDOUT.TXT
```

We added a check to see if the file exists and then we copy it to `PROGRAM.BAS`.

Let's try it out:

```sh
ngeor@ENVY170124 MINGW64 ~/Projects/temp
$ cat PROGRAM.BAS
10 PRINT "Hello, world!"
15 PRINT "Hello from me too"
20 SYSTEM

ngeor@ENVY170124 MINGW64 ~/Projects/temp
$ docker run -v $PWD:/app/basic:ro gwbasic
Hello, world!
Hello from me too
```

And from a different folder:

```sh
ngeor@ENVY170124 MINGW64 ~/Projects/temp2
$ cat PROGRAM.BAS
10 PRINT "This is a totally different file!"
20 SYSTEM

ngeor@ENVY170124 MINGW64 ~/Projects/temp2
$ docker run -v $PWD:/app/basic:ro gwbasic
This is a totally different file!
```

And with a different file name:

```sh
ngeor@ENVY170124 MINGW64 ~/Projects/temp3
$ ll
total 1
-rw-r--r-- 1 ngeor 197609 47 Feb 22 10:06 APP.BAS

ngeor@ENVY170124 MINGW64 ~/Projects/temp3
$ cat APP.BAS
10 PRINT "Starting my cool app..."
20 SYSTEM

ngeor@ENVY170124 MINGW64 ~/Projects/temp3
$ docker run -v $PWD:/app/basic:ro gwbasic
File PROGRAM.BAS not found

ngeor@ENVY170124 MINGW64 ~/Projects/temp3
$ docker run -v $PWD:/app/basic:ro gwbasic APP.BAS
Starting my cool app...
```

At this point, I'll make an alias in my `.bashrc` (I use Git Bash on Windows):

```sh
alias gwbasic='docker run --rm -v $PWD:/app/basic:ro gwbasic'
```

(Adding `--rm` to automatically remove the container once it exits and save some
disk space)

With the alias, I can simply run `gwbasic`:

```sh
ngeor@ENVY170124 MINGW64 ~/Projects/temp3
$ cat APP.BAS
10 PRINT "Starting my cool app..."
20 SYSTEM

ngeor@ENVY170124 MINGW64 ~/Projects/temp3
$ gwbasic APP.BAS
Starting my cool app...
```

## Shebang

Let's crank up the silliness a notch by supporting
[shebang](<https://en.wikipedia.org/wiki/Shebang_(Unix)>) for BAS files.

The alias won't cut it anymore, so let's create a bash script called `gwbasic`
and put it somewhere in the PATH:

```sh
#!/usr/bin/bash
docker run --rm -v $PWD:/app/basic/:ro gwbasic $1
```

And let's modify a BAS file accordingly (this one is `APP.BAS`):

```basic
#!/usr/bin/env gwbasic
10 PRINT "Starting my cool app..."
20 SYSTEM
```

If you now run `./APP.BAS`, it will hang because this isn't a valid GW-Basic
file anymore. Behind the scenes, GW-Basic is still open, reporting the syntax
error and waiting for user action, which will never come (you can kill the
Docker container with `docker stop`).

We can modify `run-dos-box.sh` to filter out the shebang line before copying the
file:

```sh
#!/bin/sh
if [ ! -r "basic/$1" ]; then
    echo "File $1 not found"
    exit 1
fi

grep -v "^#!/" "basic/$1" > PROGRAM.BAS
dosbox RUNGW.BAT -exit > /dev/null 2>&1
cat STDOUT.TXT
```

And voila:

```sh
ngeor@ENVY170124 MINGW64 ~/Projects/temp3
$ cat APP.BAS
#!/usr/bin/env gwbasic
10 PRINT "Starting my cool app..."
20 SYSTEM

ngeor@ENVY170124 MINGW64 ~/Projects/temp3
$ ./APP.BAS
Starting my cool app...
```

## Input

I remember reading a long time ago in a book, I believe it was about
[Turbo C](https://en.wikipedia.org/wiki/Borland_Turbo_C) a phrase that stuck
with me. It went along something like this: in the end, all programs accept some
input, modify it or process it, and output the results. With that in mind, let's
try to make our Basic programs process some input.

Given our DOSBox setup, we can't use stdin directly. We have to use a file, like
we did for stdout.

We modify `RUNGW.BAT`, so that it redirects stdin from a file named `STDIN.TXT`:

```bat
GWBASIC.EXE PROGRAM.BAS <STDIN.TXT >STDOUT.TXT
```

To capture stdin using Docker, we have to add the `-i` flag. However, that flag
will cause Docker to wait for input if there isn't any. So a simple "Hello,
world" program that does not require input would wait for the user to enter
something. We need to delegate the choice of whether the `-i` flag should be
added or not back to the program. We modify the `gwbasic` script to parse
parameters and add the `-i` flag only if given:

```sh
#!/usr/bin/bash

DOCKER_OPTIONS=""
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
    -i | --interactive )
        DOCKER_OPTIONS="-i"
        ;;
    * )
        echo "Unknow flag $1"
        exit 1
        ;;
esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi

docker run --rm $DOCKER_OPTIONS -v $PWD:/app/basic/:ro gwbasic $1
```

We modify `run-dos-box.sh` to capture stdin into a file named `STDIN.TXT`:

```sh
#!/bin/sh
if [ ! -r "basic/$1" ]; then
    echo "File $1 not found"
    exit 1
fi

# copy program to PROGRAM.BAS, strip shebang
grep -v "^#!/" "basic/$1" > PROGRAM.BAS

# save stdin
cat /dev/stdin > STDIN.TXT

# run it
dosbox RUNGW.BAT -exit > /dev/null 2>&1

# print stdout
cat STDOUT.TXT
```

In order to run a program that reads from stdin, we can invoke it with
`gwbasic -i APP.BAS`, and/or we can use this shebang line
`#!/usr/bin/env -S gwbasic -i`.

The following program should print its input as-is:

```basic
$ cat ECHO.BAS
#!/usr/bin/env -S gwbasic -i
10 HASMORE=1
20 WHILE HASMORE
30 LINE INPUT A$
40 IF LEN(A$)>0 THEN PRINT(A$) ELSE HASMORE=0
50 WEND
60 SYSTEM
```

Unfortunately, it prints everything double. That's because the `LINE INPUT`
command is designed for interactive mode, so it prints whatever it reads back to
the screen (which we redirected to stdout).

```sh
$ ./ECHO.BAS
Hello, world
^Z
Hello, world
Hello, world
```

So, the `stdin` redirection worked, but as soon as we use it, it ends up in the
output. Another failure. Searching around on the internet isn't going to give
millions on results on this problem, so the only workaround is to modify the
GW-Basic program to read directly from `STDIN.TXT`:

```basic
#!/usr/bin/env -S gwbasic -i
10 OPEN "STDIN.TXT" FOR INPUT ACCESS READ AS #1
20 WHILE NOT EOF(1)
30 LINE INPUT#1, A$
40 PRINT A$
50 WEND
60 CLOSE 1
70 SYSTEM
```

which works:

```sh
$ ./ECHO2.BAS
Hello, world!
^Z
Hello, world!
```

but it's a workaround nonetheless.

## Environment Variables

I was impressed to see that GW-Basic has a built-in function `ENVIRON$(name)`
which allows a program to read environment variables. We're going to try to
automatically expose all available environment variables from the top layer (my
laptop), all the way down to the GW-Basic program.

The goal is to be able to run `VERBOSE=1 gwbasic TEST.BAS` and have that script
evaluate `ENVIRON$("VERBOSE")` equal to `1`.

First, we need to pass all environment variables of the host (my laptop) to the
Docker container.

I can see all environment variables with `declare -px`:

```
declare -x SYSTEMROOT="C:\\WINDOWS"
declare -x TEMP="/tmp"
declare -x TERM="cygwin"
declare -x TMP="/tmp"
declare -x TMPDIR="/tmp"
declare -x USER
```

I want to convert this list into a one liner like `--env TEMP --env TERM` etc. A
little bit of bash magic to the rescue:

```sh
$ declare -px | grep = | sed -e 's/declare -x/--env/g' | cut -d= -f1 | grep -v PATH | tr '\n' ' '
--env SYSTEMROOT --env TEMP --env TERM --env TMP --env TMPDIR
```

I can add that to the `gwbasic` shell script which invokes Docker:

```sh
MY_ENV=`declare -px | grep = | sed -e 's/declare -x/--env/g' | cut -d= -f1 | grep -v PATH | tr '\n' ' '`
docker run --rm $DOCKER_OPTIONS $MY_ENV -v $PWD:/app/basic/:ro gwbasic $1
```

The next step is to pass the environment variables from the Docker container
into DOSBox. We're gonna modify `run-dos-box.sh` to dump the environment
variables into a Batch file named `ENV.BAT` and we're gonna modify `RUNGW.BAT`
to run `ENV.BAT` before running GW-Basic.

We'll use again `declare -px` but in this way:

```sh
# save environment variables
declare -px | grep = | grep -v PATH | sed -e 's/declare -x/SET/g' | tr -d '"' > ENV.BAT
```

Effectively it translates `declare -x KEY="VALUE"` into `SET KEY=VALUE`.

To call the batch-file, we modify `RUNGW.BAT`:

```batch
CALL ENV.BAT
GWBASIC.EXE PROGRAM.BAS <STDIN.TXT >STDOUT.TXT
```

And this is our test program:

```basic
#!/usr/bin/env gwbasic
10 PRINT "Testing environment variables"
20 IF ENVIRON$("VERBOSE")="1" THEN GOSUB 100 ELSE GOSUB 200
30 SYSTEM
100 PRINT "Verbosity has increased!"
110 RETURN
200 PRINT "I will only display essential messages"
210 RETURN
```

And it works as expected! With `VERBOSE=1`:

```
$ VERBOSE=1 ./ENV.BAS
Testing environment variables
Verbosity has increased!
```

With `VERBOSE=0`:

```
$ VERBOSE=0 ./ENV.BAS
Testing environment variables
I will only display essential messages
```

And the same without setting it at all:

```
$ ./ENV.BAS
Testing environment variables
I will only display essential messages
```

## Command Line Arguments

To the best of my knowledge, it's not possible for a GW-Basic program to read
any extra arguments from the command line. In other words,
`GWBASIC.EXE APP.BAS --verbose` isn't supported.

A workaround could be to write the CLI arguments into a pre-determined file
(like we did for `STDIN.TXT`) and then the GW-Basic program would read it, for
example one argument per line. Or, add them as environment variables.

## CGI

Back in the days, there was a protocol called
[CGI](https://en.wikipedia.org/wiki/Common_Gateway_Interface) which allowed web
servers to run programs and generate pages dynamically. By using CGI, the
payload of the request is sent to the stdin of the CGI application and the
request headers become environment variables. Good that we covered this already.
The CGI application then responds in its stdout (also covered) starting with the
response headers, a blank line, and then finally the response body.

Let's start with a different Dockerfile which is
[based on Apache HTTP Server](https://hub.docker.com/_/httpd/) (which supports
the CGI protocol). According to the instructions, we can obtain the default
`httpd.conf` configuration in order to customize it:

```sh
$ docker run --rm httpd cat /usr/local/apache2/conf/httpd.conf > my-httpd.conf
```

The goal is to serve http://localhost:8080/cgi-bin/app.bas from a GW-Basic
script outside the image. This is the Basic file:

```basic
#!/usr/bin/env gwbasic
10 PRINT "Content-Type: text/html"
20 PRINT "X-Powered-By: GW-BASIC"
30 PRINT ""
40 PRINT "<html><body><h1>GW-Basic</h1><p>It works!</p></body></html>"
50 SYSTEM
```

We need the following changes in the configuration:

1. Enable `mod_cgi.so`
2. Change `/usr/local/apache2/cgi-bin/` to `/app/basic/`

The `gwbasic` handler can be a symbolic link to `run-dos-box.sh`, so we'll just
do that in the Dockerfile, which changes like this:

```Dockerfile
FROM httpd
RUN apt-get update \
    && apt-get install -y dosbox \
    && rm -rf /var/lib/apt/lists/*
ENV SDL_VIDEODRIVER=dummy
COPY my-httpd.conf /usr/local/apache2/conf/httpd.conf
RUN mkdir /app
VOLUME [ "/app/basic" ]
COPY GWBASIC.EXE /app
COPY *.BAT /app
COPY *.sh /app
RUN ln -s /app/run-dos-box.sh /usr/bin/gwbasic
```

We'll build this image as `gwbasic-httpd`:

```sh
docker build . -t gwbasic-httpd
```

and run it with:

```sh
docker run -p 8080:80 -v $PWD:/app/basic gwbasic-httpd
```

Browsing at http://localhost:8080/ should show Apache's default "It works!"
page. Now let's try http://localhost/cgi-bin/app.bas. `httpd.conf` should map
`cgi-bin/app.bas` to `/app/basic/app.bas`, which is mounted as a volume, and
execute it.

We get an internal server error. In Apache's logs, we can see the problem:

```
10.0.2.2 - - [22/Feb/2020:13:50:12 +0000] "GET /cgi-bin/app.bas HTTP/1.1" 500 528
/usr/bin/env: 'gwbasic\r': No such file or directory
[Sat Feb 22 13:50:12.302778 2020] [cgid:error] [pid 7:tid 140158473074432] [client 10.0.2.2:53896] End of script output before headers: app.bas
```

It did find the script, but it has CRLF line endings (because GWBasic requires
it). However, Apache doesn't like that (not sure if it's Apache's fault or
`/usr/bin/env`'s fault). We're going to have to change the BAS programs to LF.
This will allow the `/usr/bin/env gwbasic` to kick in. Then, in the shell script
where we strip the shebang, we'll also convert it back to CRLF. Additionally,
we'll do the opposite transformation to `STDOUT.TXT`, converting CRLF to LF.
According to
[the internet](https://stackoverflow.com/questions/2613800/how-to-convert-dos-windows-newline-crlf-to-unix-newline-lf-in-a-bash-script),
we can use this Perl magic: `perl -pe 's/\r\n/\n/g'`.

The next problem is that Apache invokes our script with an absolute path, e.g.
`gwbasic /app/basic/APP.BAS`. This was an oversight in the previous iteration of
the shell script and it needs to be fixed. After that, there are some issues
regarding permissions (we are no longer root, but Apache uses the user `daemon`)
and another issue with DOSBox not starting because it doesn't have a `TERM`
environment variable anymore. Generally speaking, this takes some trial and
error to get it working. But when it works, it's party time:

![GW-Basic as CGI](/assets/2020/2020-02-22-16_44_07-gwbasic-cgi-bin.png)

As a lot of our temporary filenames (`STDIN.TXT`, `ENVS.BAT`, `STDOUT.TXT`,
`PROGRAM.BAS`) are unique, concurrent requests are probably something that this
setup won't be great at.

The code for this post is available
[here](https://github.com/ngeor/dockerfiles/tree/master/gwbasic).

## Let's write some BASIC!

Now that everything is in place, let's see what we can do.

You wouldn't expect to see the words "GW-Basic" and "micro-service" in the same
sentence but here we are now. Let's write a CRUD service for a to-do list (how
original), that offers some classic endpoints:

- `create.bas` - Creates a new resource
- `read.bas` - Gets an existing resource
- `update.bas` - Updates an existing resource
- `delete.bas` - Deletes an existing resource
- `list.bas` - Show all resources

To keep things simple, we will output JSON in the reading endpoints but we'll be
accepting plain text in the write endpoints. Let's start!

### create.bas

The create endpoint will:

- accept `POST` method and reject others with 405 Method not allowed
- accept `text/plain` content type and reject others with 415 Unsupported media
  type

The payload of the to-do item will be in the body of the request. If no to-do
item is given, the endpoint will return a 400 Bad Request. To-do items will be
appended to a text file named `TODO.DAT`.

```basic
#!/usr/bin/env gwbasic
10 ON ERROR GOTO 2000
20 METHOD$ = ENVIRON$("REQUEST_METHOD")
30 IF METHOD$ <> "POST" GOTO 200

40 CT$ = ENVIRON$("CONTENT_TYPE")
50 IF CT$ <> "text/plain" GOTO 300

60 OPEN "STDIN.TXT" FOR INPUT ACCESS READ AS #1
70 IF EOF(1) GOTO 90
80 LINE INPUT #1, T$
90 CLOSE #1
100 IF LEN(T$) <= 0 GOTO 400
110 OPEN "TODO.DAT" FOR APPEND AS #1
120 PRINT #1, T$
130 CLOSE #1

140 PRINT "Status: 201 Created"
150 PRINT "Content-Type: text/plain"
160 PRINT "X-Powered-By: GW-BASIC"
170 PRINT ""
180 PRINT "Processed ", T$
190 GOTO 500

200 PRINT "Status: 405 Method not allowed, send POST"
210 PRINT ""
220 GOTO 500

300 PRINT "Status: 415 Unsupported media type, I only speak text/plain"
310 PRINT ""
320 GOTO 500

400 PRINT "Status: 400 Bad request, give me one todo item"
410 PRINT ""
420 GOTO 500

500 SYSTEM

2000 PRINT "Status: 500 Internal Server Error"
2010 PRINT ""
2020 ON ERROR GOTO 0
```

### list.bas

Let's implement this one now to see if create worked. We'll print a JSON array
containing all todo items from `TODO.DAT`. This one is slightly easier:

```basic
#!/usr/bin/env gwbasic
10 ON ERROR GOTO 2000
20 METHOD$ = ENVIRON$("REQUEST_METHOD")
30 IF METHOD$ <> "GET" GOTO 200

40 PRINT "Content-Type: application/json"
50 PRINT "X-Powered-By: GW-BASIC"
60 PRINT ""
70 PRINT "["

80 OPEN "TODO.DAT" FOR INPUT AS #1
90 WHILE NOT EOF(1)
100 LINE INPUT #1, A$
110 PRINT CHR$(34) + A$ + CHR$(34)
120 IF NOT EOF(1) THEN PRINT(",")
130 WEND
140 CLOSE #1
150 PRINT "]"
160 GOTO 500

200 PRINT "Status: 405 Method not allowed, send GET"
210 PRINT ""
220 GOTO 500

500 SYSTEM

2000 PRINT "Status: 500 Internal Server Error"
2010 PRINT ""
2020 ON ERROR GOTO 0
```

### read.bas

Here we're going to read just one record. Typically these are endpoints like
`/todo/42` to return the to-do item by ID 42. Since we don't have IDs, we're
gonna use the line number (one based). The ID will be present in the query
string, so the URL will be something like `read.bas?id=42`. That will be
available in the environment variable `QUERY_STRING` as `id=2`.

```basic
#!/usr/bin/env gwbasic
10 ON ERROR GOTO 5000
20 METHOD$ = ENVIRON$("REQUEST_METHOD")
30 IF METHOD$ <> "GET" GOTO 4050

40 QS$ = ENVIRON$("QUERY_STRING")
50 IF LEFT$(QS$, 3) <> "id=" GOTO 4000
60 ID = VAL(RIGHT$(QS$, LEN(QS$) - 3))
70 IF ID <= 0 GOTO 4000

80 OPEN "TODO.DAT" FOR INPUT AS #1
90 WHILE NOT EOF(1)
100 LINE INPUT #1, A$
110 ID = ID - 1
120 IF ID = 0 GOTO 140
130 WEND
140 CLOSE #1
150 IF ID <> 0 GOTO 4040

160 PRINT "Content-Type: application/json"
170 PRINT "X-Powered-By: GW-BASIC"
180 PRINT ""
190 PRINT "{" + CHR$(34) + "item" + CHR$(34) + ": " + CHR$(34) + A$ + CHR$(34) + "}"
200 GOTO 9999

4000 PRINT "Status: 400 Bad request"
4001 PRINT ""
4002 GOTO 9999

4040 PRINT "Status: 404 Not found"
4041 PRINT ""
4042 GOTO 9999

4050 PRINT "Status: 405 Method not allowed, send GET"
4051 PRINT ""
4052 GOTO 9999

5000 PRINT "Status: 500 Internal Server Error"
5001 PRINT ""
5002 ON ERROR GOTO 0

9999 SYSTEM
```

As the numbering starts becoming tiresome, I started a convention:

- line 9999 is the final exit to the system
- HTTP error codes jump to the line of the error code followed by a zero (e.g.
  line 4040 is HTTP 404)

The endpoint gives 400 if the id is invalid or missing and 404 if no such item
exists.

### update.bas

The update endpoint will be called with the `id` query string parameter to
indicate which item we wish to update. The updated value for the todo item will
be in the body of the request in plain text.

The technique involves renaming the data file to a different temporary name and
then recreating it, updating the value only for the requested item.

```basic
#!/usr/bin/env gwbasic
10 ON ERROR GOTO 5000
20 METHOD$ = ENVIRON$("REQUEST_METHOD")
30 IF METHOD$ <> "POST" GOTO 4050

40 CT$ = ENVIRON$("CONTENT_TYPE")
50 IF CT$ <> "text/plain" GOTO 4150

60 QS$ = ENVIRON$("QUERY_STRING")
70 IF LEFT$(QS$, 3) <> "id=" GOTO 4000
80 ID = VAL(RIGHT$(QS$, LEN(QS$) - 3))
90 IF ID <= 0 GOTO 4000

100 OPEN "STDIN.TXT" FOR INPUT ACCESS READ AS #1
110 IF EOF(1) GOTO 4000
120 LINE INPUT #1, T$
130 CLOSE #1
140 IF LEN(T$) <= 0 GOTO 4000

150 NAME "TODO.DAT" AS "TODO.OLD"
160 OPEN "TODO.OLD" FOR INPUT AS #1
170 OPEN "TODO.DAT" FOR OUTPUT AS #2
180 WHILE NOT EOF(1)
190 LINE INPUT #1, A$
200 ID = ID - 1
210 IF ID = 0 THEN Z$ = T$ ELSE Z$ = A$
220 PRINT #2, Z$
230 WEND
240 CLOSE #1
250 CLOSE #2
260 KILL "TODO.OLD"
270 IF ID > 0 GOTO 4040

280 PRINT "Content-Type: text/plain"
290 PRINT "X-Powered-By: GW-BASIC"
300 PRINT ""
310 GOTO 9999

4000 PRINT "Status: 400 Bad request"
4001 PRINT ""
4002 GOTO 9999

4040 PRINT "Status: 404 Not found"
4041 PRINT ""
4042 GOTO 9999

4050 PRINT "Status: 405 Method not allowed, send POST"
4051 PRINT ""
4052 GOTO 9999

4150 PRINT "Status: 415 Unsupported media type, I only speak text/plain"
4151 PRINT ""
4152 GOTO 9999

5000 PRINT "Status: 500 Internal Server Error"
5001 PRINT ""
5002 ON ERROR GOTO 0

9999 SYSTEM
```

### delete.bas

Finally, the delete endpoint is similar to the update, but instead of updating a
value, it skips it when recreating the new file. It also listens only to the
`DELETE` verb.

```basic
#!/usr/bin/env gwbasic
10 ON ERROR GOTO 5000
20 METHOD$ = ENVIRON$("REQUEST_METHOD")
30 IF METHOD$ <> "DELETE" GOTO 4050

40 QS$ = ENVIRON$("QUERY_STRING")
50 IF LEFT$(QS$, 3) <> "id=" GOTO 4000
60 ID = VAL(RIGHT$(QS$, LEN(QS$) - 3))
70 IF ID <= 0 GOTO 4000

80 NAME "TODO.DAT" AS "TODO.OLD"
90 OPEN "TODO.OLD" FOR INPUT AS #1
100 OPEN "TODO.DAT" FOR OUTPUT AS #2
110 WHILE NOT EOF(1)
120 LINE INPUT #1, A$
130 ID = ID - 1
140 IF ID <> 0 THEN PRINT #2, A$
150 WEND
160 CLOSE #1
170 CLOSE #2
180 KILL "TODO.OLD"
190 IF ID > 0 GOTO 4040

200 PRINT "Content-Type: text/plain"
210 PRINT "X-Powered-By: GW-BASIC"
220 PRINT ""
230 GOTO 9999

4000 PRINT "Status: 400 Bad request"
4001 PRINT ""
4002 GOTO 9999

4040 PRINT "Status: 404 Not found"
4041 PRINT ""
4042 GOTO 9999

4050 PRINT "Status: 405 Method not allowed, send POST"
4051 PRINT ""
4052 GOTO 9999

4150 PRINT "Status: 415 Unsupported media type, I only speak text/plain"
4151 PRINT ""
4152 GOTO 9999

5000 PRINT "Status: 500 Internal Server Error"
5001 PRINT ""
5002 ON ERROR GOTO 0

9999 SYSTEM
```

### Final touch: mod_rewrite

To make the REST API a bit more RESTful, we can active `mod_rewrite` in Apache
and configure it like this

```

RewriteEngine on

RewriteCond "%{REQUEST_METHOD}" "GET"
RewriteRule "^/api/todo$" "/cgi-bin/list.bas" [PT]

RewriteCond "%{REQUEST_METHOD}" "POST"
RewriteRule "^/api/todo$" "/cgi-bin/create.bas" [PT]

RewriteCond "%{REQUEST_METHOD}" "GET"
RewriteRule "^/api/todo/([0-9]+)$" "/cgi-bin/read.bas?id=$1" [PT]

RewriteCond "%{REQUEST_METHOD}" "POST"
RewriteRule "^/api/todo/([0-9]+)$" "/cgi-bin/update.bas?id=$1" [PT]

RewriteCond "%{REQUEST_METHOD}" "DELETE"
RewriteRule "^/api/todo/([0-9]+)$" "/cgi-bin/delete.bas?id=$1" [PT]
```

which makes our API more RESTful with these endpoints:

- List all: `GET /api/todo`
- Create: `POST /api/todo`
- Read: `GET /api/todo/{id}`
- Update: `POST /api/todo/{id}`
- Delete: `DELETE /api/todo/{id}`

## TL;DR

The 80s called and they brought `GOTO` statements and line numbers.

Computer -> Docker -> DOSBox -> GWBasic.exe

Browser -> Computer -> Docker -> Apache -> DOSBox -> GWBasic.exe

With a lot of bash glue in between.
