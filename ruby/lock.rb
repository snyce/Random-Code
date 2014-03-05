#!/usr/bin/env ruby

while true do
  pid = fork do 
    Signal.trap("INT") do
      puts "Trapped Kill..."
      continue
    end
  end
end
