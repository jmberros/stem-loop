#! /usr/bin/env ruby
# encoding: utf-8

require './stem-loop'

if __FILE__ == $0
  input = ARGV.empty? ? ARGF.readlines.map(&:chomp) : ARGV
  input.each { |stockholm| Infernal.new.cmbuild stockholm }
end
