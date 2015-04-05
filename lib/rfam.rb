class Rfam
  def download_stockholm(accession)
    filename = "#{accession}.sto"
    puts "\n 🌐 Download the Multiple Sequence Alignment with accession code #{accession}"
    `curl --silent -o #{filename} #{url(accession)}`

    # Scan for a sequence ID to give a more meaningful name to the file
    id = `cat #{filename} | grep "#=GF ID" | awk '{ print $NF }'`.chomp
    unless id.empty?
      original_filename = filename
      filename = "#{id}." + filename
      `mv "#{original_filename}" #{filename}`
    end

    puts " ✔ #{filename}".green.bold
    filename
  end

  private

  def url(accession)
    "http://rfam.xfam.org/family/#{accession}/alignment?"\
    "acc=#{accession}&format=stockholm&download=1"
  end
end

