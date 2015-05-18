#!/usr/bin/env ruby
# -*- encoding: utf-8 -*-

require 'csv'

ret = {}

CSV.foreach("all-results.csv") do |row|
  scaffold = row[0]
  model = row[2]
  accession = row[3]
  ret[scaffold] ||= []
  ret[scaffold] << "#{model}__(#{accession})"
end

ret.each do |k, v|
  puts "#{k} #{v.join(" ")}"
end
