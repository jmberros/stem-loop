#!/usr/bin/env ruby
# encoding: UTF-8

require 'fileutils'
require 'colorize'

class Rfam
  def download_stockholms(accessions=nil)
    FileUtils.mkdir target_dir unless File.exists? target_dir
    Dir.chdir target_dir

    Array(accessions).each do |accession|
      puts "\n Downloading #{accession} from:\n #{url(accession)}"
      `curl --silent -o #{accession}.sto #{url(accession)}`
      id = `cat #{accession}.sto | grep "#=GF ID" | awk '{ print $NF }'`.chomp
      filename = "#{id}.#{accession}.sto"
      FileUtils.mv "#{accession}.sto", filename
      puts " ↪ #{filename}".green.bold
    end

    puts happy_cat "Done! Check the directory `./#{target_dir}` for your files"
  end

  private

  def target_dir
    "stockholms"
  end

  def url(accession)
    "http://rfam.xfam.org/family/#{accession}/alignment?"\
    "acc=#{accession}&format=stockholm&download=1"
  end
end

def debug(message)
  p message if ENV["DEBUG"]
end

def happy_cat(message)
  "\n 😸 --( #{message} )"
end

def sad_cat(message)
  "\n 🙀 --( #{message} )"
end

if __FILE__ == $0
  abort(sad_cat "Feed me Rfam accession codes separated by a space") if ARGV.empty?

  Rfam.new.download_stockholms(ARGV)
end
