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

