#!/usr/bin/env perl
use strict;
use warnings;
use POSIX qw(strftime);

my @date = gmtime;

print "What is the title of the post? ";
my $title = <STDIN>;
chomp $title;
return unless ($title);
my $slug         = lc($title =~ s/ /-/gr);
my $file         = strftime "_posts/%Y/%Y-%m-%d-$slug.md", @date;
my $fm_date      = strftime "%Y-%m-%d %H:%M:%S", @date;
my $front_matter = <<HERE;
---
layout: post
title: $title
date: $fm_date
---

HERE

open(my $fh, '>', $file) or die "Could not write file $file $!";
print $fh $front_matter;
close($fh);
