#!/usr/bin/env ruby
# frozen_string_literal: true

require('psych')

def collect_posts(dir)
  result = []
  Dir.children(dir).each do |child|
    full_path = File.join(dir, child)
    if File.directory?(full_path)
      result += collect_posts(full_path)
    else
      result << full_path
    end
  end
  result
end

def delete_files(dir, exceptions)
  Dir.children(dir).map { |f| File.join(dir, f) }.each do |child|
    File.delete(child) unless exceptions.include?(child)
  end
end

class PageInfo
  # Creates an instance of this class.
  # title: The title of the tag
  # post_count: How many posts are tagged with this tag
  # total_count: The total number of posts
  def initialize(title, post_count, total_count)
    @title = title
    @post_count = post_count
    max_len = total_count.to_s.length
    all_nines = ('9' * max_len).to_i
    fmt = "%0#{max_len}d" # %05d
    @sort_index = "#{format(fmt, all_nines - post_count)}-#{title.downcase}"
  end

  attr_reader :title
  attr_reader :post_count
  attr_reader :sort_index

  def to_s
    "#{@title} (#{@post_count}) #{@sort_index}"
  end
end

class PageInfoCollection
  def initialize
    @map = {}
    @total_count = 0
  end

  def add(value)
    @map[value] = if @map[value]
                    @map[value] + 1
                  else
                    1
                  end

    puts "Warning: tag #{value} exists in case variations" if @map.keys.index { |k| k.casecmp?(value) && k != value }
  end

  def add_post
    @total_count += 1
  end

  def to_s
    @map.keys.map { |k| "#{k} => #{@map[k]}" }.reduce { |memo, obj| "#{memo}, #{obj}" }
  end

  def to_sorted_array
    @map.keys.map { |k| PageInfo.new(k, @map[k], @total_count) }.sort_by(&:sort_index)
  end
end

class Collector
  def initialize
    @tags = PageInfoCollection.new
  end

  attr_reader :tags

  def add(front_matter)
    @tags.add_post
    front_matter['tags']&.each { |t| @tags.add(t) }
  end

  def to_s
    "tags=[#{@tags}]"
  end
end

def tag_title_to_tag_url_segment(tag)
  norm = tag.tr(' ', '-').downcase.sub('.net', '-dot-net').sub('.', '-').sub('#', '-sharp').sub('++', '-plus-plus').sub('!', '')
  norm = norm[1..norm.length] if norm.start_with?('-')
  norm
end

def create_tag_page(pi)
  tag = pi.title
  normalized_tag = tag_title_to_tag_url_segment(tag)
  fullpath = File.join('_by_tag', "#{normalized_tag}.md")
  File.open(fullpath, 'w:UTF-8') do |f|
    f.puts(<<~HERE
      ---
      layout: tag
      permalink: /archives/tag/#{normalized_tag}/
      title: Posts tagged with #{tag}
      tag: #{tag}
      post_count: #{pi.post_count}
      sort_index: #{pi.sort_index}
      ---
      {% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
      {%- include post-list.html -%}
      HERE
    )
  end
  fullpath
end

def main
  posts = collect_posts('_posts')
  puts "Found #{posts.length} posts"
  collector = Collector.new
  posts.each do |p|
    collector.add(Psych.load_file(p))
  end

  created_tag_files = collector.tags.to_sorted_array.map do |pi|
    create_tag_page(pi)
  end
  delete_files '_by_tag', created_tag_files
end

main
