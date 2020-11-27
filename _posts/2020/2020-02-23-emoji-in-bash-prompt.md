---
layout: post
title: Emoji in bash prompt
date: 2020-02-23 08:08:51 +02:00
tags:
  - bash
  - emoji
---

I saw this in a colleague's laptop the other day. He had his bash prompt
configured to show a black arrow when things are okay and a red arrow when the
last command failed. I fiddled around with my bash prompt to achieve something
similar.

This is for Mac by the way, but hopefully that shouldn't be too important.
Originally, I had setup my `.bash_profile` to use the git prompt:

```sh
. /Library/Developer/CommandLineTools/usr/share/git-core/git-completion.bash
. /Library/Developer/CommandLineTools/usr/share/git-core/git-prompt.sh

PS1='\h: \W $(__git_ps1 " (%s)") \u\$ '
```

To display colors (another thing I was missing), I had to change the `PS1` line
into `PROMPT_COMMAND`:

```sh
GIT_PS1_SHOWCOLORHINTS="1"
PROMPT_COMMAND='__git_ps1 "\u@\h:\w" "\\\$ "'
```

As `__git_ps1` is just a function that sets `PS1`, I added my own function in
`.bash_profile`:

```sh
__last_err_ps1() {
  local EXIT="$?"
  local RCol='\[\e[0m\]'
  local Red='\[\e[0;31m\]'
  if [ $EXIT != 0 ]; then
    PS1="🚨 ${Red}${EXIT}${RCol} ${PS1}"
  else
    PS1="🆗 ${PS1}"
  fi
}
```

This function checks the exit code and prepends a text to the PS1 prompt. If the
exit code is zero, it adds the OK emoji. Otherwise, it adds an alarm emoji and
also shows the exit code in red. I find the visual hint quite useful and showing
the exit code saves the extra effort of typing `echo $?` to see it.

To use it, I modified `PROMPT_COMMAND` into:

```sh
PROMPT_COMMAND='__git_ps1 "\u@\h:\w" "\\\$ " ; __last_err_ps1'
```

Here's how it looks like on a terminal:

![Emoji in bash prompt](/assets/2020/2020-02-23-emoji-bash.png)

Hope this helps!
