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
  def initialize(title, post_count, total_count)
    @title = title
    @post_count = post_count
    @sort_index = "#{format('%05d', total_count - post_count)}-#{title.downcase}"
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
    @categories = PageInfoCollection.new
    @tags = PageInfoCollection.new
  end

  attr_reader :categories
  attr_reader :tags

  def add(front_matter)
    front_matter['categories']&.each { |c| @categories.add(c) }
    front_matter['tags']&.each { |t| @tags.add(t) }
  end

  def to_s
    "categories=[#{@categories}], tags=[#{@tags}]"
  end
end

def create_category_page(pi, config)
  fullpath = File.join('_category', "#{pi.title}.md")
  category_config = config['categories'][pi.title]
  title = category_config['title'] if category_config
  title = pi.title.tr('-', ' ').split(/(\W)/).map(&:capitalize).join unless title && !title.empty?
  description = category_config['description'] if category_config
  File.open(fullpath, 'w:UTF-8') do |f|
    f.puts('---')
    f.puts('layout: category')
    f.puts("url_segment: #{pi.title}")
    f.puts("title: #{title}")
    f.puts("post_count: #{pi.post_count}")
    f.puts("sort_index: #{pi.sort_index}")
    category_config&.each { |k, v| f.puts("#{k}: #{v}") if k != 'title' && k != 'description' }
    f.puts('---')
    if description
      f.puts('')
      f.puts(description)
    end
  end
  fullpath
end

def tag_title_to_tag_url_segment(tag)
  norm = tag.tr(' ', '-').downcase.sub('.net', '-dot-net').sub('.', '-').sub('#', '-sharp').sub('++', '-plus-plus').sub('!', '')
  norm = norm[1..norm.length] if norm.start_with?('-')
  norm
end

def create_tag_page(pi)
  tag = pi.title
  normalized_tag = tag_title_to_tag_url_segment(tag)
  fullpath = File.join('_tag', "#{normalized_tag}.md")
  File.open(fullpath, 'w:UTF-8') do |f|
    f.puts('---')
    f.puts('layout: tag')
    f.puts("url_segment: #{normalized_tag}")
    f.puts("title: #{tag}")
    f.puts("post_count: #{pi.post_count}")
    f.puts("sort_index: #{pi.sort_index}")
    f.puts('---')
  end
  fullpath
end

def main
  config = Psych.load_file('_config.yml')
  posts = collect_posts('_posts')
  collector = Collector.new
  posts.each do |p|
    collector.add(Psych.load_file(p))
  end

  created_category_files = collector.categories.to_sorted_array.map do |pi|
    create_category_page(pi, config)
  end
  delete_files '_category', created_category_files

  created_tag_files = collector.tags.to_sorted_array.map do |pi|
    create_tag_page(pi)
  end
  delete_files '_tag', created_tag_files
end

main
