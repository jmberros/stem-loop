#!/usr/bin/env ruby
# encoding: utf-8

require_relative '../stem-loop'

if __FILE__ == $0
  options = {}
  OptionParser.new do |opts|
    opts.banner = "Usage: #{__FILE__}.rb [options]"

    opts.on("--cpu=N", "Use n cores") do |cpu|
      options[:cpu] = cpu
    end

    opts.on("-h", "--help", "Prints this help") do
      puts opts
      exit
    end
  end.parse!

  input = ARGV.empty? ? ARGF.readlines.map(&:chomp) : ARGV
  calibration_manager = CalibrationManager.new

  input.each do |covariance_model|
    job_filename = calibration_manager.write_script covariance_model, options[:cpu]

    puts job_filename unless $stdout.tty?
  end
end

