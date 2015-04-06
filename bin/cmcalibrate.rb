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

  ARGF.each_line do |line|
    covariance_model = line.chomp
    calibrated_model = Infernal.new.calibrate covariance_model, options[:cpu]
    puts calibrated_model unless $stdout.tty?
  end
end
