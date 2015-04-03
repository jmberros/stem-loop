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

    successful_calibration = !`cat #{covariance_model} | grep "ECM"`.empty?
    if successful_calibration
      new_filename = covariance_model.gsub(".cm", ".c.cm")
      FileUtils.mv "#{covariance_model}", new_filename
      t1 = Time.now
      elapsed = distance_of_time_in_words(t0, t1)
      puts " ↪ #{new_filename} (completed in #{elapsed})".green
    else
      puts " ↪ It seems the calibration was unsuccessful. Check the file.".red
    end
  end

  def forecast_calibration(covariance_model)
    command = "cmcalibrate --nforecast 6 --forecast #{covariance_model} | "\
              "grep -v '^#' | grep -v 'ok' | awk '{ print $2 }'"
    predicted_time = `#{command}`.chomp
    puts " ⌚ Expected duration of ~#{predicted_time} (hh:mm:ss)"
  end
end

if __FILE__ == $0
  input = ARGV.empty? ? ARGF.readlines.map(&:chomp) : ARGV
  input.each { |covariance_model| Infernal.new.calibrate covariance_model }
end
