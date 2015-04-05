class Infernal
  def cmbuild(stockholm_filename)
    cm_filename = stockholm_filename.gsub ".sto", ".cm"

    puts "\n ⚒ Build a Covariance Model for the MSA in '#{stockholm_filename}'"
    `cmbuild -F #{cm_filename} #{stockholm_filename}`

    puts " ✔ #{cm_filename}".green.bold
    cm_filename
  end

  def calibrate(covariance_model, run=true)
    puts "\n Calibrate the Covariance Model in '#{covariance_model}'"

    forecast_calibration "#{covariance_model}"
    command = "cmcalibrate --cpu 6 #{covariance_model}"  

    if run
      t0 = Time.now
      puts " ⚒ Begin calibration at #{t0.strftime("%H:%M")}".yellow
      `#{command}`
      successful_calibration = !`cat #{covariance_model} | grep "ECM"`.empty?

      if successful_calibration
        new_filename = covariance_model.gsub(".cm", ".c.cm")
        FileUtils.mv "#{covariance_model}", new_filename
        t1 = Time.now
        #elapsed = distance_of_time_in_words(t0, t1)
        elapsed = t1 - t0 # TODO: Make seconds human-readable
        puts " ✔ [ok] #{new_filename} (completed in #{elapsed})".green
        new_filename
      else
        puts " ☹ [fail] It seems the calibration was unsuccessful. Check the file.".red
      end
    else
      command
    end
  end

  def forecast_calibration(covariance_model)
    command = "cmcalibrate --nforecast 6 --forecast #{covariance_model} | "\
              "grep -v '^#' | grep -v 'ok' | awk '{ print $2 }'"
    predicted_time = `#{command}`.chomp
    puts " ⌚ Expected duration of ~#{predicted_time} (hh:mm:ss)"
  end
end

