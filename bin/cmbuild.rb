#! /usr/bin/env ruby
# encoding: utf-8

require_relative '../stem-loop'


if __FILE__ == $0
  input = ARGV.empty? ? ARGF.readlines.map(&:chomp) : ARGV
  infernal = Infernal.new
  input.each do |stockholm|
    covariance_model = infernal.cmbuild stockholm

    if $stdout.tty?
      infernal.forecast_calibration covariance_model
    else # When piping, just pass the built model filename
      puts covariance_model
    end
  end
end
