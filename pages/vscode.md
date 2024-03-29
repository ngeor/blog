---
layout: page
title: Visual Studio Code
date: 2019-01-10
---

Extensions, themes and configuration for Visual Studio Code.

## Extensions

- AsciiDoc
- [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)
- Cucumber (Gherkin) Full Support
- docker
- EditorConfig for VS Code
- ESLint
- Font Switcher
- GitLens
- Go
- Jira and Bitbucket (Official)
- LaTeX Workshop
- [PlantUML](https://github.com/qjebbs/vscode-plantuml)
- Prettier - Code formatter
- Python
- Rust (rls)
- SCSS Formatter
- Todo Tree
- TSLint
- XML
- YAML

## Themes

- Atom One Dark Theme
- Atom One Light Theme
- Ayu
- bluloco-light
- Brackets Light Pro
- Cobalt2 Theme Official
- Eva Theme
- GitHub Plus Theme
- NetBeans Light Theme
- Night Owl
- Snazzy Light
- Xcode Default

## Configuration

```json
{
  // Disable telemetry
  "telemetry.enableTelemetry": false,

  // Do not ask confirmation to sync with git
  "git.confirmSync": false,

  // Trim trailing whitespace
  "files.trimTrailingWhitespace": true,

  // Trim extra empty lines at the end of the file
  "files.trimFinalNewlines": true,

  // Insert final new line (EOL at EOF)
  "files.insertFinalNewline": true,

  // A wide selection of fonts to choose from
  "editor.fontFamily": "'Andale Mono', 'Anonymous Pro', CamingoCode, 'Cascadia Code', Consolas, 'Courier New', 'Courier Prime Code', 'DejaVu Sans Mono', 'Droid Sans Mono', 'Envy Code R', 'Fantasque Sans Mono', 'Fira Code', 'Go Mono', Hack, Iosevka, Inconsolata, 'Input Mono', 'Liberation Mono', 'Lucida Console', 'Meslo LG S', Monaco, monofur, Monoid, mononoki, 'Operator Mono Light', 'PT Mono', 'Roboto Mono', 'Source Code Pro', 'Segoe UI Mono'",

  // Auto-format document on save
  "editor.formatOnSave": true,

  // Override Python auto-format indentation,
  // e.g. indent Python files with 2 spaces instead of 4
  "python.formatting.autopep8Args": ["--indent-size=2"],

  // Configure ESLint extension to check TypeScript files too
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    {
      "language": "typescript",
      "autoFix": true
    }
  ],

  // set the default terminal to git bash
  "terminal.integrated.shell.windows": "C:\\Program Files\\Git\\bin\\bash.exe",

  // auto-wrap markdown paragraphs
  "prettier.proseWrap": "always",

  // set default formatter for HTML
  "[html]": {
    "editor.defaultFormatter": "vscode.html-language-features"
  }
}
```

## Reset

To reset VS Code, delete the folders `~/.vscode` and `%APPDATA%/Code`.

Settings are in `%APPDATA%/Code/User/settings.json` and snippets in
`%APPDATA%/Code/User/snippets`.
