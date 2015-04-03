#!/usr/bin/env ruby
# encoding: utf-8

require 'rubygems'
require 'colorize'
require 'action_view'
include ActionView::Helpers::DateHelper

class Infernal
  def calibrate(covariance_model)
    puts "\n Calibrate the Covariance Model in '#{covariance_model}'"

    t0 = Time.now
    puts " ⚒ Begin calibration at #{t0.strftime("%H:%M")}".yellow
    forecast_calibration "#{covariance_model}"
    `cmcalibrate --cpu 6 #{covariance_model}`  

    t1 = Time.now
    elapsed = distance_of_time_in_words(t0, t1)
    puts " ↪ Finished at #{t1.strftime("%H:%M")} (elapsed time: #{elapsed})".green
  end

  def forecast_calibration(covariance_model)
    command = "cmcalibrate --nforecast 6 --forecast #{covariance_model} | "\
              "grep -v '^#' | grep -v 'ok' | awk '{ print $2 }'"
    predicted_time = `#{command}`.chomp
    puts " ⌚ Expected duration of ~#{predicted_time} (hh:mm:ss)"
  end
end

if __FILE__ == $0
  infernal = Infernal.new

  # Read arguments from the command line
  ARGV.each { |covariance_model| infernal.calibrate covariance_model }

  # Feed from standard input
  while covariance_model = gets do infernal.calibrate covariance_model.chomp end
end
