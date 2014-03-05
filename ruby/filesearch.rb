#!/usr/bin/env ruby

require 'find'

print "Enter search path: "
searchpath = gets.chomp()
print "Enter Pattern: "
searchpattern = gets.chomp()
print "Searching #{searchpath} for #{searchpattern}...\n\n"

Find.find(searchpath) do |path|
    if FileTest.directory?(path)
        if File.basename(path)[0] == ?.
            Find.prune
        else
            next
        end
    else
        if File.fnmatch(searchpattern, File.basename(path))
            print "Filename: %s\n" % File.basename(path)
            print "Filename: %s\n" % File.basename(path).full_name
            print "Permissions\t: %s\n" % File.stat(path).mode
            print "UID\t: %s\n" % File.stat(path).uid
            print "GID\t: %s\n" % File.stat(path).gid
            print "Size\t: %s\n" % File.stat(path).size
            print "\n"
        end 
     end
end
