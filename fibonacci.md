---
layout: page
title: Fibonacci
permalink: /fibonacci/
---

Write a program that prints the first N numbers of the
[Fibonacci sequence](https://en.wikipedia.org/wiki/Fibonacci_number).
F<sub>0</sub> = 0, F<sub>1</sub> = 1 and F<sub>n</sub> = F<sub>n-1</sub> +
F<sub>n-2</sub>.

I made this page with a bit of [MS-DOS](https://en.wikipedia.org/wiki/MS-DOS)
nostalgia, showing a solution to the Fibonacci quiz in some of my earliest
programming languages (if you're curious, I have
[more Fibonacci implementations](https://github.com/ngeor/fibonacci)).

Click on a screenshot to see the solution:

  <ul class="selector">
    <li>
      <input type="checkbox" id="gwbasic" />
      <label for="gwbasic" class="selector" title="GW-Basic">
        <figure>
          <img alt="GW-Basic" src="/assets/fibonacci/gwbasic.png">
          <figcaption>GW-Basic</figcaption>
        </figure>
      </label>
      <div markdown="1" class="code">

```
10 PRINT "Enter N to calculate fibonacci"
20 INPUT N
30 PRINT "You entered: ", N
40 F0 = 0
50 F1 = 1
60 FOR I = 0 TO N
70 IF I = 0 THEN F = F0 ELSE IF I = 1 THEN F = F1 ELSE F = PREV1 + PREV2
80 PRINT "Fib of ", I, "IS", F
90 REM Shift values
100 PREV2 = PREV1
110 PREV1 = F
120 NEXT I
```

From [Wikipedia](https://en.wikipedia.org/wiki/GW-BASIC):

> GW-BASIC is a dialect of the BASIC programming language developed by Microsoft
> from IBM BASICA.
>
> [...]
>
> All IF/THEN/ELSE conditional statements must be written on one line.
>
> [...]
>
> First appeared: 1983

</div>
    </li>
    <li>
      <input type="checkbox" id="qbasic" />
      <label for="qbasic" class="selector" title="QBasic">
        <figure>
          <img alt="QBasic" src="/assets/fibonacci/qbasic.png">
          <figcaption>QBasic</figcaption>
        </figure>
      </label>
<div markdown="1" class="code">

```vb
DECLARE FUNCTION Fib! (N!)
PRINT "Enter the number of fibonacci to calculate"
INPUT N
FOR I = 0 TO N
  PRINT "Fibonacci of ", I, " is ", Fib(I)
NEXT

FUNCTION Fib (N)
  IF N <= 1 THEN
    Fib = N
  ELSE
    Fib = Fib(N - 1) + Fib(N - 2)
  END IF
END FUNCTION
```

From [Wikipedia](https://en.wikipedia.org/wiki/QBasic):

> QBasic, a short form of Quick Beginners All purpose Symbolic Instruction Code,
> is an integrated development environment (IDE) and interpreter for a variety
> of BASIC programming languages which are based on QuickBASIC
>
> [...]
>
> QBasic was intended as a replacement for GW-BASIC.
>
> [...]
>
> First appeared: 1991

</div>
    </li>
    <li>
      <input type="checkbox" id="pascal" />
      <label for="pascal" class="selector" title="Turbo Pascal">
        <figure>
          <img alt="Turbo Pascal" src="/assets/fibonacci/pascal.png">
          <figcaption>Turbo Pascal</figcaption>
        </figure>
      </label>
<div markdown="1" class="code">

```pascal
program Fibonacci;

function fib(n: Integer): Integer;
begin
  if n <= 1 then
    fib := n
  else
    fib := fib(n - 1) + fib(n - 2);
end;

var
  i, n: Integer;
begin
  Write('Enter the N to calculate the fibonacci ');
  ReadLn(n);
  for i := 0 to n do
    WriteLn('Fibonacci of ', i, ' is ', fib(i));
end.
```

From [Wikipedia](https://en.wikipedia.org/wiki/Turbo_Pascal):

> Turbo Pascal is a software development system that includes a compiler and an
> integrated development environment (IDE) for the Pascal programming language
> running on CP/M, CP/M-86, and DOS. It was originally developed by Anders
> Hejlsberg at Borland, and was notable for its extremely fast compiling times.
> Turbo Pascal, and the later but similar Turbo C, made Borland a leader in
> PC-based development.
>
> [...]
>
> First appeared: 1983

I used Turbo Pascal 6, which was released in 1990 (according to
[progopedia](http://progopedia.com/version/turbo-pascal-6.0/)).

</div>

  </li>
</ul>
