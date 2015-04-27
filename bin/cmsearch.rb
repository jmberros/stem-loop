#! /usr/bin/env ruby
# encoding: utf-8

require_relative '../stem-loop'

def main
  Dir["*.c.cm"].each do |covariance_model|
    ( Dir["*.fa"] + Dir["*.fna"] ).each do |fasta|

      filename =
        "#{covariance_model.gsub(".c.cm", "")}__in__#{fasta.gsub(".fa", "")}"

      $logger.debug "➡ cmsearch #{covariance_model} in #{fasta}"

      `cmsearch --tblout #{filename}.cmsearch.tbl #{covariance_model} #{fasta} > #{filename}.cmsearch-output`
    end
  end
end


main if __FILE__ == $0

