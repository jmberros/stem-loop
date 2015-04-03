#! /usr/bin/env ruby
# encoding: utf-8

require 'colorize'

def cmbuild(stockholm_filename)
  name = stockholm_filename.gsub ".sto", ""

  puts "\n Build Covariance Model for '#{stockholm_filename}'"
  `cmbuild -F #{name}.cm #{name}.sto` # | tee #{name}.cm.log`

  puts " ↪ #{name}.cm".green.bold
       #"\n ( There's a log of the process in #{name}.cm.log )"

  forecast_calibration "#{name}.cm"
end

def forecast_calibration(cm_filename)
  puts "\n Forecast Calibration of '#{cm_filename}'"
  command = "cmcalibrate --nforecast 6 --forecast #{cm_filename} | "\
            "grep -v '^#' | grep -v 'ok' | awk '{ print $2 }'"
  predicted_time = `#{command}`.chomp
  puts " ↪ calibration should take ~#{predicted_time} (hh:mm:ss)".blue.bold
end

if __FILE__ == $0
  abort(" 😸 Feed me one or more stockholm filenames") if ARGV.empty?

  ARGV.each { |stockholm| cmbuild stockholm }
end
