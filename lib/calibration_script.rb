class CalibrationScript
  def write_script(covariance_model)
    puts " ✎ Generate PBS job script to calibrate #{covariance_model}"

    options = default_options.merge({
      job_name: "#{File.basename(covariance_model)}_calibration",
      covariance_model: covariance_model,
      new_filename: covariance_model.gsub(".cm", ".c.cm")
    })

    job_script_filename = covariance_model.gsub(".cm", ".cm.calibrate.job")
    File.open(job_script_filename, "w+") do |file|
      file.puts Mustache.render( File.read(template_path), options )
    end

    puts " ↪ #{job_script_filename}".green.bold
  end

  private

  def template_path
    "./templates/calibration-job.mustache"
  end

  def default_options
    {
      queue_name: 'default',
      nodes: 1,
      cores: 1,
      mail: "juanmaberros@gmail.com" # Hardcoded email? C'mon ...
    }
  end
end

