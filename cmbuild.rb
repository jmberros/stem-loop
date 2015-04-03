#! /usr/bin/env ruby
# encoding: utf-8

require 'colorize'

class Infernal
  def cmbuild(stockholm_filename)
    name = stockholm_filename.gsub ".sto", ""

    puts "\n Build Covariance Model for '#{stockholm_filename}'"
    `cmbuild -F #{name}.cm #{name}.sto` # | tee #{name}.cm.log`

    puts " ↪ #{name}.cm".green.bold
        #"\n ( There's a log of the process in #{name}.cm.log )"

    forecast_calibration "#{name}.cm"
  end

  def forecast_calibration(cm_filename)
    command = "cmcalibrate --nforecast 6 --forecast #{cm_filename} | "\
              "grep -v '^#' | grep -v 'ok' | awk '{ print $2 }'"
    predicted_time = `#{command}`.chomp
    puts " ↪ ~#{predicted_time} (hh:mm:ss) to calibrate".blue.bold
  end
end

if __FILE__ == $0
  infernal = Infernal.new

  # Read arguments from the command line
  ARGV.each { |stockholm| infernal.cmbuild stockholm }

  # Feed from standard input
  while stockholm = gets do infernal.cmbuild stockholm.chomp end
end
