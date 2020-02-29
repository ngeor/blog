---
layout: post
title: Strip the BOM
date: 2017-08-02 07:03:25.000000000 +02:00
published: true
tags:
- bom
- gulp
- nodejs
- Visual Studio
---

The <a href="https://en.wikipedia.org/wiki/Byte_order_mark" target="_blank" rel="noopener">byte order mark</a>, or BOM for short, is a special Unicode character that can be used to indicate that a file's contents is Unicode. Visual Studio is one of those editors that like to use the BOM when saving UTF-8 files. There are a few problems with the BOM. It can break shell scripts, as it precedes the <a href="https://en.wikipedia.org/wiki/Shebang_(Unix)" target="_blank" rel="noopener">shebang</a>. It can cause unnecessary diff noise in git history, just like any other invisible character mismatch (spaces vs tabs, different line endings, lack of EOL at EOF). In short, I don't like it and I'd like to get rid of it.

<!--more-->

I was working on a Yeoman generator that creates a C# project, so this BOM issue was annoying at unit tests. Some source files had the BOM while their corresponding expected files didn't. As usual in the JavaScript world, there's a npm package that solves the problem. I added the package <a href="https://github.com/lichunqiang/gulp-stripbom" target="_blank" rel="noopener">gulp-stripbom</a> and this is how it looks like in my <code>gulpfile.js</code>:

```

const stripBom = require('gulp-stripbom');

gulp.task('stripbom', function() {
return gulp.src(['**/*.*', '!node_modules/**'])
    .pipe(stripBom())
    .pipe(gulp.dest('.'));
});

```

<em>Side note</em>: I started using gulp instead of grunt and I find it a bit better. A common problem with gulp and grunt tasks is that documentation is spread over the tasks and the libraries they're wrapping. I think gulp gives you more flexibility and I like its streams. <em>End of side note</em>.

This gulp task just removes the BOM character from all files in the project, case closed.

I do have other projects however which don't use gulp or JavaScript for that matter. How do I do a one time cleanup to get rid of the BOM character?

I poked around in the dependencies of gulp-stripbom and I found it's using the <a href="https://github.com/sindresorhus/strip-bom" target="_blank" rel="noopener">strip-bom</a> package, which is essentially <a href="https://github.com/sindresorhus/strip-bom/blob/master/index.js" target="_blank" rel="noopener">a very simple function</a>. There's also the <a href="https://github.com/sindresorhus/strip-bom-cli" target="_blank" rel="noopener">strip-bom-cli</a> package, but it doesn't edit files in-place.

I ended up writing this long bash line:

```

$ find . -type f -iname "*.cs" -exec node -e "var f = process.argv[1]; var contents = fs.readFileSync(f, 'utf8'); if (contents.charCodeAt(0) === 0xFEFF) { fs.writeFileSync(f, contents.slice(1), 'utf8'); } " \{\} \;

```

Disclaimer: You should have a backup. Better try this on a git directory, so that you can rollback if needed.

What does this code do? It uses <code>find</code> to find all files I want to change (*.cs) and runs the given inline node script (<code>node -e</code>) for every match.

The node script can be reviewed easier if I format it in multiple lines:

```

var f = process.argv[1]; // get the filename passed as parameter to the node script by find
var contents = fs.readFileSync(f, 'utf8'); // read the file contents in utf8
if (contents.charCodeAt(0) === 0xFEFF) { // if the first character the BOM?
    fs.writeFileSync(f, contents.slice(1), 'utf8'); // save the file, stripping the first character
}

```

This way is suboptimal, as it launches a separate node process for each file, but I don't care for a one time cleanup.

If I do <code>git diff</code> I can see the invisible BOM:

```

$ git diff
diff --git a/NGSoftware.Common/IStoppable.cs b/NGSoftware.Common/IStoppable.cs
index bb592a5..c13522d 100644
--- a/NGSoftware.Common/IStoppable.cs
+++ b/NGSoftware.Common/IStoppable.cs
@@ -1,4 +1,4 @@
-<U+FEFF>using System;
+using System;
using System.Threading;

```

It's the U+FEFF character being removed. I'm not sure if it's also visible when reviewing a pull request on a browser.

For JavaScript files, you can also use ESLint to prevent the usage BOM with the <a href="http://eslint.org/docs/rules/unicode-bom" target="_blank" rel="noopener">unicode-bom rule</a>.
