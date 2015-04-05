#!/usr/bin/env ruby
# encoding: utf-8

require_relative '../stem-loop'


if __FILE__ == $0
  input = ARGV.empty? ? ARGF.readlines.map(&:chomp) : ARGV
  input.each do |accession_code|
    StemLoop.download_sto_build_cm_enqueue_calibration accession_code 
  end
end