#!/usr/bin/env ruby
#-*- encoding: utf-8 -*-

require "fileutils"

Dir["*.cm"].each do |covariance_model|
  is_calibrated = !`cat #{covariance_model} | grep "ECM"`.empty?
  new_filename = covariance_model.gsub(".cm", ".c.cm")
  if is_calibrated
    FileUtils.mv "#{covariance_model}", new_filename
    puts " #{covariance_model} → #{new_filename}"
  end
end
