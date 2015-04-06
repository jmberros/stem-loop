class Infernal
  def cmbuild(stockholm_filename)
    cm_filename = stockholm_filename.gsub ".sto", ".cm"
    abort(" ☹  File #{stockholm_filename} doesn't exist?") unless File.exist? stockholm_filename

    $logger.debug "\n ⚒ Build a Covariance Model for the MSA in '#{stockholm_filename}'"
    `cmbuild -F #{cm_filename} #{stockholm_filename}`

    $logger.debug " ✔ #{cm_filename}".green.bold
    cm_filename
  end

  def calibrate(covariance_model, cores=1)
    $logger.debug "\n Calibrate the Covariance Model in '#{covariance_model}'"

    predicted_time = forecast_calibration covariance_model, cores
    $logger.debug " ⌚ Expected calibration of #{predicted_time} (h:m:s) with #{cores} core(s)"

    t0 = Time.now
    $logger.debug " ⚖ Begin calibration at #{t0.strftime("%H:%M")}".yellow
    `cmcalibrate --cpu #{cores} #{covariance_model}` # This takes some time

    successful_calibration = !`cat #{covariance_model} | grep "ECM"`.empty?

    if successful_calibration
      new_filename = covariance_model.gsub(".cm", ".c.cm")
      FileUtils.mv "#{covariance_model}", new_filename
      t1 = Time.now
      elapsed = $utils.time_in_words(t1 - t0)
      $logger.debug " ✔ #{new_filename} (completed in #{elapsed})".green
      new_filename
    else
      $logger.debug " ☹ [fail] It seems the calibration was unsuccessful.".red
    end
  end

  def forecast_calibration(covariance_model, cores=1)
    command = \
      "cmcalibrate --nforecast #{cores} --forecast #{covariance_model} | "\
      "grep -v '^#' | grep -v 'ok' | awk '{ print $2 }'"
    `#{command}`.chomp
  end
end

