#!/usr/bin/env ruby
# encoding: utf-8

require_relative '../stem-loop'

if __FILE__ == $0
  input = ARGV.empty? ? ARGF.readlines.map(&:chomp) : ARGV
  calibration_manager = CalibrationManager.new

  input.each do |covariance_model|
    job_filename = calibration_manager.write_script covariance_model 
    server_response = calibration_manager.enqueue_job job_filename

    puts server_response unless $stdout.tty?
  end
end

