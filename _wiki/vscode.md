---
layout: page
title: Visual Studio Code
---

Extensions, themes and configuration for Visual Studio Code.

Extensions
----------

- Code Spell Checker
- EditorConfig
- Font Switcher
- Markdown Table Formatter
- Rewrap

#### Language Specific

- ESLint
- Python
- TSLint

Themes
------

- Atom One Light Theme
- Cobalt2 Theme Official
- Night Owl

Fonts
-----

- Envy Code R

Configuration
-------------

- Disable telemetry

```
  "telemetry.enableTelemetry": false,
```

- Don't ask for syncing with git

```
  "git.confirmSync": false
```

- Indent Python files with 2 spaces instead of 4

```
  "python.formatting.autopep8Args": [
    "--indent-size=2"
  ]
```

- Trim trailing whitespace

```
  "files.trimTrailingWhitespace": true,
```

- Trim extra empty lines at the end of the file

```
  "files.trimFinalNewlines": true,
```

- Insert final new line (EOL at EOF)

```
  "files.insertFinalNewline": true
```
