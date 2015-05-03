#! /usr/bin/env ruby
# encoding: utf-8

require_relative '../stem-loop'

def main(opts={})
  opts[:max] = ARGV.any? { |arg| arg == '--max' }
  fastas = Dir["*.fa"] + Dir["*.fna"]
  models = Dir["*.c.cm"]

  fail "[!] No FASTAs found in this directory (.fa or .fna)" if fastas.empty?
  fail "[!] No models found in this directory (.c.cm)" if models.empty?

  models.each do |covariance_model|
    fastas.each do |fasta|

      filename =
        "#{covariance_model.gsub(".c.cm", "")}__in__#{fasta.gsub(".fa", "")}"

      $logger.debug "➡ cmsearch #{covariance_model} in #{fasta}"

      `cmsearch #{'--max' if opts[:max]} --tblout #{filename}.cmsearch.tbl #{covariance_model} #{fasta} > #{filename}.cmsearch-output`
    end
  end
end


main if __FILE__ == $0

