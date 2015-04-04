#!/usr/bin/env ruby
# encoding: UTF-8

require './stem-loop'

if __FILE__ == $0
  input = ARGV.empty? ? ARGF.readlines.map(&:chomp) : ARGV
  input.each { |accession| Rfam.new.download_stockholm accession }
end
