class Rfam
  def download_stockholm(accession)
    $logger.debug "\n 🌐 Download the Multiple Sequence Alignment with "\
                  "accession code #{accession}"

    filename = "#{accession}.sto"
    `curl --silent -o #{filename} #{url(accession)}`

    # Scan for a sequence ID to give a more meaningful name to the file
    id = `cat #{filename} | grep "#=GF ID" | awk '{ print $NF }'`.chomp
    unless id.empty?
      original_filename = filename
      filename = "#{id}." + filename
      `mv "#{original_filename}" #{filename}`
    end

    $logger.debug " ✔ #{filename}".green.bold
    filename
  end

  private

  def url(accession)
    "http://rfam.xfam.org/family/#{accession}/alignment?"\
    "acc=#{accession}&format=stockholm&download=1"
  end
end

