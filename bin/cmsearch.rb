#! /usr/bin/env ruby
# encoding: utf-8

require_relative '../stem-loop'

def main(opts={})
  opts[:max] = ARGV.any? { |arg| arg == '--max' } # TODO: This should be optparsed earlier
  fastas = Dir["*.fa"] + Dir["*.fna"]
  models = Dir["*.c.cm*"]

  puts "[!] No FASTAs found in this directory (.fa or .fna)" if fastas.empty?
  puts "[!] No models found in this directory (.c.cm)" if models.empty?
  exit if fastas.empty? || models.empty?

  models.each do |covariance_model|
    fastas.each do |fasta|

      filename =
        "#{covariance_model.gsub(".c.cm", "")}__in__#{fasta.gsub(".fa", "")}"

      $logger.debug "➡ cmsearch #{covariance_model} in #{fasta}"

      `cmsearch --tblout #{filename}.cmsearch.tbl \
       #{'--max' if opts[:max]} #{'--cpu ' + opts[:cpu] if opts[:cpu]} \
       #{covariance_model} #{fasta} > #{filename}.cmsearch-output`
    end
  end
end

if __FILE__ == $0
  options = {}
  OptionParser.new do |opts|
    opts.banner = "Usage: #{__FILE__}.rb [options]"

    opts.on("--cpu=N", "Use n cores") do |cpu|
      options[:cpu] = cpu
    end

    opts.on("-h", "--help", "Prints this help") do
      puts opts
      exit
    end
  end.parse!

  main(options)
end

