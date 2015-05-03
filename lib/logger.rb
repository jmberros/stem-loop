class Logger
  def debug(message)
    puts "\n#{message}" if $stdout.tty? # Doesn't print help messages when piping

    #message = message.gsub("\n", "").chomp.strip
    #File.open(logfile, "a+") do |f|
      #f.puts "[ #{script} ][ #{time_formatted} ] #{message}"
    #end
  end

  private

  # These used to log to a file named after the script
  #def logfile
    #"stem-loop.#{script}.log"
  #end

  #def time_formatted
    #Time.now.strftime("%A %d %B, %H:%M:%S.%L")
  #end

  #def script
    #File.basename($PROGRAM_NAME).gsub(".rb", "")
  #end
end
