---
layout: page
title: IntelliJ IDEA
---

Extensions, themes and configuration for IntelliJ IDEA.

## Plugins

- [ANTLR v4 grammar plugin](https://plugins.jetbrains.com/plugin/7358-antlr-v4-grammar-plugin/)
- [AsciiDoc](https://plugins.jetbrains.com/plugin/7391-asciidoc/)
- [CheckStyle-IDEA](https://plugins.jetbrains.com/plugin/1065-checkstyle-idea/)
- [HashiCorp Terraform / HCL language support](https://plugins.jetbrains.com/plugin/7808-hashicorp-terraform--hcl-language-support/)
- [RoboPOJOGenerator](https://plugins.jetbrains.com/plugin/8634-robopojogenerator/)
- [Scala](https://plugins.jetbrains.com/plugin/1347-scala/)

## Configuration

### Checkstyle

Configured to use the latest and greatest of my custom rules:
https://raw.githubusercontent.com/ngeor/checkstyle-rules/master/src/main/resources/com/github/ngeor/checkstyle.xml

### Imports

Some tweaks to align with Checkstyle. The settings are available at: Editor ->
Code Style -> Java -> Imports

Set to an arbitrary large number to avoid star imports:

- Class count to use import with '\*': 50
- Names count to use static import with '\*': 50

Import layout:

- Layout static imports separately: Yes
- `import java.*` with subpackages
- `import javax.*` with subpackages
- `import org.*` with subpackages
- blank line
- import all other imports
- blank line
- import static all other imports

### Automatically download Maven documentation

Build -> Build Tools -> Maven -> Importing

Check automatically download sources and documentation

## Reset

To reset IntelliJ IDEA, delete the folder starting with `.Idea` in your home
folder.

For example, on the current version the folder is named `.IdeaIC2019.2`.
