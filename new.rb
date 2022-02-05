#!/usr/bin/env ruby

require('time')
now = Time.now

print 'What is the title of the post? '
title = gets.strip
return if title.empty?

slug = title.downcase.tr(' ', '-')
year = now.strftime('%Y')
folder = "_posts/#{year}"
Dir.mkdir(folder) unless Dir.exist?(folder)
filename = "#{folder}/#{now.strftime('%Y-%m-%d')}-#{slug}.md"
fm_date = now.strftime('%Y-%m-%d %H:%M:%S')
front_matter = <<~HERE
  ---
  layout: post
  title: #{title}
  date: #{fm_date}
  ---
HERE

File.open(filename, 'w') { |f| f.write(front_matter) }
