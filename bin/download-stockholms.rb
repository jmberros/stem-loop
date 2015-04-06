#!/usr/bin/env ruby
# encoding: UTF-8

require_relative '../stem-loop'

if __FILE__ == $0
  ARGF.each_line do |line|
    accession_code = line.chomp
    stockholm_file = Rfam.new.download_stockholm accession_code
    puts stockholm_file unless $stdout.tty?
  end
end
