#!/usr/bin/env ruby

require 'socket'
require 'optparse'

host = ARGV[0]
port = ARGV[1]

if !host:
  print "Enter host: "
  host = gets.chomp()
end

if !port:
  print "Enter port: "
  port = gets.chomp()
end

host = 'localhost' if host.empty?
port = 80 if port.empty?

puts "\nHost: #{host} Port: #{port}\n\n"

TCPSocket.open(host, port) do |socket|
  socket.puts "GET / HTTP/1.0\n\n"
  puts socket.read
  socket.close
end
