---
layout: post
title: Windows Docker and paths
date: 2019-12-25 06:58:33
categories:
  - tech
tags:
  - Docker Toolbox
  - docker
  - Windows
  - Git Bash
---

I use [Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_windows/)
at home, as my laptop is running Windows Home and therefore cannot run Docker
Desktop. Sometimes, mounting volumes can get tricky.

Let's say that I'm working on a project and I want to try it out from within a
Docker container. If I open up Docker Quickstart Terminal and run the following,
everything works as expected (i.e. the current directory is mounted as `/code`
inside my container):

```
docker run --rm -v $(pwd):/code -w /code -it perl bash
```

Most of the time though, I'll open up my usual terminal or a terminal embedded
in my IDE. In that case, the same command fails:

```
C:\Program Files\Docker Toolbox\docker.exe: Error response from daemon: the working
directory 'C:/Program Files/Git/code' is invalid, it needs to be an absolute path.
See 'C:\Program Files\Docker Toolbox\docker.exe run --help'.
```

Although I passed `-w /code` to set the working directory, Docker thinks I
passed `C:/Program Files/Git/code`. If I remove the `-w` argument and keep just
the volume, I get a similar error:

```
C:\Program Files\Docker Toolbox\docker.exe: Error response from daemon: invalid mode: \Program Files\Git\code.
See 'C:\Program Files\Docker Toolbox\docker.exe run --help'.
```

To overcome this, we need this variable:

```
MSYS_NO_PATHCONV=1
```

For example, this succeeds:

```
MSYS_NO_PATHCONV=1 docker run --rm -v $(pwd):/code -w /code -it perl bash
```

But why does it work from within Docker Quickstart Terminal? The answer lies in
the script `C:\Program Files\Docker Toolbox\start.sh`. It defines `docker` as a
function:

```sh
docker () {
  MSYS_NO_PATHCONV=1 docker.exe "$@"
}
export -f docker
```

which sets the environment variable and calls the Docker executable. By adding the same snippet in `.bashrc`, Docker behaves the same everywhere.
