#!/usr/bin/env ruby
# encoding: UTF-8

require_relative '../stem-loop'

if __FILE__ == $0
  input = ARGV.empty? ? ARGF.readlines.map(&:chomp) : ARGV

  input.each do |accession|
    stockholm_file = Rfam.new.download_stockholm accession
    puts stockholm_file unless $stdout.tty?
  end
end
