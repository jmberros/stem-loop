#! /usr/bin/env ruby
# encoding: utf-8

require_relative '../stem-loop'


if __FILE__ == $0
  input = ARGV.empty? ? ARGF.readlines.map(&:chomp) : ARGV
  infernal = Infernal.new
  input.each do |stockholm|
    covariance_model = infernal.cmbuild stockholm
    infernal.forecast_calibration covariance_model
  end
end
