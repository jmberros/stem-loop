#! /usr/bin/env ruby
# encoding: utf-8

require 'colorize'

class Infernal
  def cmbuild(stockholm_filename)
    name = stockholm_filename.gsub ".sto", ""

    puts "\n Build a Covariance Model for the MSA in '#{stockholm_filename}'"
    `cmbuild -F #{name}.cm #{name}.sto` # | tee #{name}.cm.log`

    puts " ↪ #{name}.cm".green.bold
        #"\n ( There's a log of the process in #{name}.cm.log )"
  end
end

if __FILE__ == $0
  infernal = Infernal.new

  # Read arguments from the command line
  ARGV.each { |stockholm| infernal.cmbuild stockholm }

  # Feed from standard input
  while stockholm = gets do infernal.cmbuild stockholm.chomp end
end
