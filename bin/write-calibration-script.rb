#!/usr/bin/env ruby
# encoding: utf-8

require_relative '../stem-loop'


if __FILE__ == $0
  input = ARGV.empty? ? ARGF.readlines.map(&:chomp) : ARGV
  input.each { |covariance_model| CalibrationScript.new.write_script covariance_model }
end
