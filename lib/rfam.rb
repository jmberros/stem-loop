class Rfam
  def download_stockholm(accession)
    $logger.debug "🌐 Download stockholm file for #{accession}"

    filename = "#{accession}.sto"
    `curl --silent -o #{filename} #{url(accession)}`
    filename = rename_from_metadata(filename)

    $logger.debug "✔ #{filename}".green
    filename
  end

  def rename_from_metadata(filename)
    # Scan for an ID or NAME to give a more meaningful filename
    # ID is found in stockholms, NAME is found in covariance models

    # Quit if it's a CM database
    return if `cat #{filename} | grep NAME | wc -l`.chomp.to_i > 2

    id = `cat #{filename} | grep "#=GF ID" | head -n1 | awk '{ print $NF }'`.chomp
    name = `cat #{filename} | grep "NAME" | head -n1 | awk '{ print $NF }'`.chomp
    id = id.empty? ? nil : id
    name = name.empty? ? nil : name

    if id || name
      new_filename = "#{id || name}." + filename
      `mv #{filename} #{new_filename}`
    end
    new_filename || filename
  end

  private

  def url(accession)
    "http://rfam.xfam.org/family/#{accession}/alignment?"\
    "acc=#{accession}&format=stockholm&download=1"
  end
end

