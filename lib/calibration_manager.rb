class CalibrationManager
  def write_script(covariance_model, cores=1)
    abort(" ⚠ File #{covariance_model} doesn't exist") unless File.exist? covariance_model
    $logger.debug "\n ✎ Generate PBS job script to calibrate #{covariance_model}"

    job_filename = covariance_model.gsub(".cm", ".cm.calibrate.job")
    options = default_options.merge({
      cmcalibrate_path: `which cmcalibrate`.chomp,
      cores: cores,
      job_name: "calibrate__#{File.basename(covariance_model)}",
      covariance_model: covariance_model,
      output_filename: "#{job_filename}.output",
      error_filename: "#{job_filename}.errors",
      new_filename: covariance_model.gsub(".cm", ".c.cm"),
    })

    File.open(job_filename, "w+") do |file|
      file.puts Mustache.render( File.read(template_path), options )
    end

    $logger.debug " ✔ #{job_filename}".green
    job_filename
  end

  def enqueue_job(job_filename)
    $logger.debug "\n ⌛ Enqueue the calibration job"
    server_response = `qsub #{job_filename}`.chomp
    $logger.debug " ↪ #{server_response}"

    predicted_time = Infernal.new.forecast_calibration(covariance_model, 1)
    $logger.debug " ⌚ Expected calibration of #{predicted_time} (h:m:s) with #{cores} core(s)"

    server_response
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

