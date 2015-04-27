#!/usr/bin/env ruby
# encoding: UTF-8

require_relative '../stem-loop'

if __FILE__ == $0
  rfam = Rfam.new
  files = Dir["*.stockholm"] + Dir["*.stockholm.txt"] + Dir[".sto"] + \
          Dir["*.cm"] + Dir["*.c.cm"]
  files.uniq.each { |filename| puts rfam.rename_from_metadata(filename) }
end

