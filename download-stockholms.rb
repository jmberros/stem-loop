#!/usr/bin/env ruby
# encoding: UTF-8

require 'fileutils'
require 'colorize'

class Rfam
  def download_stockholm(accession)
    puts "\n 🌐 Download the Multiple Sequence Alignment with accession code #{accession}"
    `curl --silent -o #{accession}.sto #{url(accession)}`
    id = `cat #{accession}.sto | grep "#=GF ID" | awk '{ print $NF }'`.chomp
    filename = "#{id}.#{accession}.sto"
    FileUtils.mv "#{accession}.sto", filename
    puts " ↪ #{filename}".green.bold
  end

  private

  def url(accession)
    "http://rfam.xfam.org/family/#{accession}/alignment?"\
    "acc=#{accession}&format=stockholm&download=1"
  end
end

if __FILE__ == $0
  input = ARGV.empty? ? ARGF.readlines.map(&:chomp) : ARGV
  input.each { |accession| Rfam.new.download_stockholm accession }
end
