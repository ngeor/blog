---
layout: post
title: Thread-safe code
date: 2011-06-05 07:04:00.000000000 +02:00
type: post
parent_id: '0'
published: true
categories:
- Tech Notes
tags: []
author: Nikolaos Georgiou
---

Consider this code:

```
if (!dictionary.ContainsKey(key)) {
  dictionary.Add(key, value);
}
```

In a multithreaded environment, thread A and B may check for the existence of the key at the same time and both determine that the key doesn’t exist. Then, they both try to add it. One of them gets the ArgumentException about the key  already been there, because the other thread just added it.
<table border="1">
<tbody>
<tr>
<td></td>
<td>Thread A</td>
<td>Thread B</td>
</tr>
<tr>
<td>1</td>
<td>ContainsKey (returns false)</td>
<td>ContainsKey (returns false)</td>
</tr>
<tr>
<td>2</td>
<td>Add</td>
<td>Add</td>
</tr>
</tbody>
</table>

.NET collections are not synchronized as you know. So the above table shows the two threads happily running in parallel.

What I saw in my project's code is that in some cases the problem was "solved" by using a ThreadSafeDictionary in place of the standard .NET Dictionary class. This custom ThreadSafeDictionary class has synchronized methods. However, this doesn’t actually solve the problem. Consider these possible execution paths:

Thread B gets exception:
<table border="1">
<tbody>
<tr>
<td></td>
<td>Thread A</td>
<td>Thread B</td>
</tr>
<tr>
<td>1</td>
<td>ContainsKey (returns false)</td>
<td>Blocked by Thread A</td>
</tr>
<tr>
<td>2</td>
<td>Waits for system to resume Thread A</td>
<td>ContainsKey (return false)</td>
</tr>
<tr>
<td>3</td>
<td>Add (ok)</td>
<td>Blocked by Thread A</td>
</tr>
<tr>
<td>4</td>
<td></td>
<td>Add (exception)</td>
</tr>
</tbody>
</table>

No exception scenario (if you’re lucky):
<table border="1">
<tbody>
<tr>
<td></td>
<td>Thread A</td>
<td>Thread B</td>
</tr>
<tr>
<td>1</td>
<td>ContainsKey (returns false)</td>
<td>Blocked by Thread A</td>
</tr>
<tr>
<td>2</td>
<td>Add (ok)</td>
<td>ContainsKey (return true)</td>
</tr>
</tbody>
</table>

Thread A gets exception:
<table border="1">
<tbody>
<tr>
<td></td>
<td>Thread A</td>
<td>Thread B</td>
</tr>
<tr>
<td>1</td>
<td>ContainsKey (returns false)</td>
<td>Blocked by Thread A</td>
</tr>
<tr>
<td>2</td>
<td>Waits for system to resume Thread A</td>
<td>ContainsKey (return false)</td>
</tr>
<tr>
<td>3</td>
<td>Blocked by Thread B</td>
<td>Add (ok)</td>
</tr>
<tr>
<td>4</td>
<td>Add (exception)</td>
<td></td>
</tr>
</tbody>
</table>

Another one:
<table border="1">
<tbody>
<tr>
<td></td>
<td>Thread A</td>
<td>Thread B</td>
</tr>
<tr>
<td>1</td>
<td>ContainsKey (returns false)</td>
<td>Blocked by Thread A</td>
</tr>
<tr>
<td>2</td>
<td>Add (ok)</td>
<td>ContainsKey (return false because Add of Thread A hasn’t quite finished yet)</td>
</tr>
<tr>
<td>3</td>
<td></td>
<td>Add (exception)</td>
</tr>
</tbody>
</table>

So the problem is not solved. Why? While the ContainsKey and Add methods of the ThreadSafeDictionary are thread-safe on their own,  the business logic that they create combined isn’t.  What you need to do, is to lock your entire block of code that needs to be ran by one thread at a time. This is called the <a href="http://en.wikipedia.org/wiki/Critical_section" target="_blank">Critical Section</a>. The above code should be written like:

```
lock (synchronizeObject) {
  if (!dictionary.ContainsKey(key)) {
    dictionary.Add(key, value);
  }
}
```

This way you lock the entire code block for single thread access and you ensure your data integrity. And, the critical section should be as big as necessary but not more.

The issue becomes more serious for structures that have a long life time (e.g. application scope), which increases the chances of failure over time.
