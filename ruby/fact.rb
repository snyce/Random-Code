#!/usr/bin/env ruby -w

require "profile"

def fact(n)
  n > 1 ? n * fact(n -1) : 1
end
fact(627)
