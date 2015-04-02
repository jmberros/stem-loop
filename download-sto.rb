#!/usr/bin/env ruby

# TODO: Resque or Sidekiq worker classes
# Downloader, Builder, Calibrator, 
class StemLoop
  attr_accessor :accessions

  def initialize
    @accessions = []
  end

  def download_stockholms
    @accessions.each do |accession|
      url = "http://rfam.xfam.org/family/RF01998/alignment?"\
            "acc=#{accession}&format=stockholm&download=1"

      # Create /stockholm destination dir
      # Assign destination path in that dir with accession code
      # Download to destination path
    end
  end

  def cmbuild
    @accessions.each do |accession|
      # `cmbuild #{accession}.cm #{accession}.sto`
    end
  end

  def cmcalibrate
    @accessions.each do |accession|
      # `cmbuild #{accession}.cm #{accession}.sto`
    end
  end
end
