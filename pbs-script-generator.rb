#!/usr/bin/env ruby
# encoding: utf-8

require './stem-loop'

class CalibrationScript
  def write_script(covariance_model)
    script = File.open covariance_model.gsub(".cm", ".cm.calibrate.job"), "w+"
    new_filename = covariance_model.gsub(".cm", ".c.cm")
    Mustache.template_file = template_path
    script.puts Mustache.render File.read(template_path), options(covariance_model)
    script.close

    puts " ✎ Generate PBS job script to calibrate #{covariance_model}"
    puts " ↪ #{File.basename script.path}".green.bold
  end

  private

  def template_path
    "./templates/pbs_script.mustache"
  end

  def options(covariance_model)
    default_options.merge({
      job_name: "#{covariance_model}_calibration",
      covariance_model: covariance_model
    })
  end

  def default_options
    {
      queue_name: 'default',
      nodes: 1,
      cores: 1,
      mail: "juanmaberros@gmail.com"
    }
  end
end


if __FILE__ == $0
  input = ARGV.empty? ? ARGF.readlines.map(&:chomp) : ARGV
  input.each { |covariance_model| CalibrationScript.new.write_script covariance_model }
end
