#!/usr/bin/env ruby -w

abort "Please specify a file!" if ARGV.empty?

file = ARGV[0]

File.open(file) do |x|
    x.each {|line| puts line.reverse }
end
