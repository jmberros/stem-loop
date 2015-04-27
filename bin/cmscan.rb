#! /usr/bin/env ruby
# encoding: utf-8

require_relative '../stem-loop'

def main
  Dir["*.c.cm"].each do |covariance_model|
    Dir["*.fa"].each do |fasta|

      filename =
        "#{covariance_model.gsub(".c.cm", "")}__in__#{fasta.gsub(".fa", "")}"

      $logger.debug "➡ cmscan #{covariance_model} in #{fasta}"

      `cmscan --tblout #{filename}.cmscan.tbl #{covariance_model} #{fasta} > #{filename}.cmscan-output`
    end
  end
end


main if __FILE__ == $0


