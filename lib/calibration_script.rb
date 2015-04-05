class CalibrationScript
  def write_script(covariance_model, run=false)
    abort(" ⚠ File #{covariance_model} doesn't exist") unless File.exist? covariance_model
    puts "\n ✎ Generate PBS job script to calibrate #{covariance_model}"

    job_script_filename = covariance_model.gsub(".cm", ".cm.calibrate.job")
    options = default_options.merge({
      cmcalibrate_path: `which cmcalibrate`.chomp,
      cores: 1, # TODO: Configurable
      job_name: "calibrate__#{File.basename(covariance_model)}",
      covariance_model: covariance_model,
      output_filename: "#{job_script_filename}.output",
      error_filename: "#{job_script_filename}.errors",
      new_filename: covariance_model.gsub(".cm", ".c.cm"),
    })

    File.open(job_script_filename, "w+") do |file|
      file.puts Mustache.render( File.read(template_path), options )
    end

    puts " ✔ #{job_script_filename}".green.bold

    enqueue(job_script_filename) if run
    Infernal.new.forecast_calibration(covariance_model, 1)
    job_script_filename
  end

  def enqueue(job_script_filename)
    puts "\n ⌛ Enqueue the calibration job"
    server_response = `qsub #{job_script_filename}`.chomp
    puts " ↪ #{server_response}".blue.bold
  end

  private

  def template_path
    "#{APP_ROOT}/templates/calibration-job.mustache"
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

